import os
import hashlib
import hmac
from typing import Optional
import razorpay
from src.models.payment_model import PaymentModel
from dotenv import load_dotenv

load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

# Initialize Razorpay
razorpay_client = None
if RAZORPAY_KEY_ID and RAZORPAY_SECRET:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))


class PaymentService:
    """Payment service for Razorpay integration"""

    @staticmethod
    async def createOrder(
        user_id: str, amount: float, currency: str = "INR", options: dict = None
    ) -> dict:
        """Create Razorpay order"""
        if not razorpay_client:
            raise ValueError("Razorpay not configured")

        order_options = {
            "amount": int(amount * 100),  # Convert to paise
            "currency": currency,
            "receipt": f"receipt_{int(__import__('time').time() * 1000)}",
            **(options or {}),
        }

        try:
            # Create order in Razorpay
            razorpay_order = razorpay_client.order.create(order_options)

            # Save payment record in database
            payment = await PaymentModel.create(
                {
                    "user_id": user_id,
                    "amount": amount,
                    "currency": currency,
                    "provider_payment_id": razorpay_order["id"],
                    "status": "pending",
                    "meta": {
                        "razorpay_order": razorpay_order,
                        **(options or {}),
                    },
                }
            )

            return {
                "payment": payment,
                "razorpay_order": {
                    "id": razorpay_order["id"],
                    "amount": razorpay_order["amount"],
                    "currency": razorpay_order["currency"],
                    "receipt": razorpay_order["receipt"],
                    "status": razorpay_order["status"],
                    "key_id": RAZORPAY_KEY_ID,  # Frontend needs this
                },
            }
        except Exception as e:
            raise ValueError(f"Failed to create payment order: {str(e)}")

    @staticmethod
    def verifyPaymentSignature(order_id: str, payment_id: str, signature: str) -> bool:
        """Verify Razorpay payment signature"""
        if not RAZORPAY_SECRET:
            raise ValueError("Razorpay secret not configured")

        text = f"{order_id}|{payment_id}"
        generated_signature = hmac.new(
            RAZORPAY_SECRET.encode(), text.encode(), hashlib.sha256
        ).hexdigest()

        return generated_signature == signature

    @staticmethod
    async def verifyPayment(payload: dict) -> dict:
        """Verify and update payment status"""
        order_id = payload.get("razorpay_order_id")
        payment_id = payload.get("razorpay_payment_id")
        signature = payload.get("razorpay_signature")

        if not all([order_id, payment_id, signature]):
            raise ValueError("Missing required payment fields")

        # Verify signature
        if not PaymentService.verifyPaymentSignature(order_id, payment_id, signature):
            raise ValueError("Invalid payment signature")

        # Find payment by provider order ID
        payment = await PaymentModel.findByProviderId(order_id)
        if not payment:
            raise ValueError("Payment not found")

        # Update payment status
        updated_payment = await PaymentModel.update(
            payment["id"],
            {
                "status": "completed",
                "provider_payment_id": payment_id,
                "meta": {
                    **payment.get("meta", {}),
                    "razorpay_payment_id": payment_id,
                    "razorpay_signature": signature,
                    "verified_at": __import__("datetime").datetime.utcnow().isoformat(),
                    **{k: v for k, v in payload.items() if k not in ["razorpay_order_id", "razorpay_payment_id", "razorpay_signature"]},
                },
            },
        )

        return updated_payment

    @staticmethod
    async def handleWebhook(payload: dict, signature: str) -> dict:
        """Handle Razorpay webhook"""
        if not RAZORPAY_SECRET:
            raise ValueError("Razorpay secret not configured")

        # Verify webhook signature
        import json
        text = json.dumps(payload, separators=(",", ":"))
        generated_signature = hmac.new(
            RAZORPAY_SECRET.encode(), text.encode(), hashlib.sha256
        ).hexdigest()

        if generated_signature != signature:
            raise ValueError("Invalid webhook signature")

        event = payload.get("event")
        payment_data = (
            payload.get("payload", {})
            .get("payment", {})
            .get("entity")
            or payload.get("payload", {}).get("order", {}).get("entity")
        )

        if event in ["payment.captured", "payment.authorized"]:
            # Find payment and update status
            payment_id = payment_data.get("order_id") or payment_data.get("id")
            payment = await PaymentModel.findByProviderId(payment_id)

            if payment:
                await PaymentModel.update(
                    payment["id"],
                    {
                        "status": "completed",
                        "provider_payment_id": payment_data.get("id"),
                        "meta": {
                            **payment.get("meta", {}),
                            "webhook_data": payload,
                            "webhook_event": event,
                        },
                    },
                )
        elif event == "payment.failed":
            payment_id = payment_data.get("order_id") or payment_data.get("id")
            payment = await PaymentModel.findByProviderId(payment_id)

            if payment:
                await PaymentModel.update(
                    payment["id"],
                    {
                        "status": "failed",
                        "meta": {
                            **payment.get("meta", {}),
                            "webhook_data": payload,
                            "webhook_event": event,
                        },
                    },
                )

        return {"processed": True, "event": event}

    @staticmethod
    async def getPaymentById(id: str) -> dict:
        """Get payment by ID"""
        payment = await PaymentModel.findById(id)
        if not payment:
            raise ValueError("Payment not found")
        return payment

    @staticmethod
    async def getPaymentsByUserId(
        user_id: str, limit: int = 50, offset: int = 0
    ) -> list:
        """Get payments by user ID"""
        return await PaymentModel.findByUserId(user_id, limit, offset)

