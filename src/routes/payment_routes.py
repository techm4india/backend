from fastapi import APIRouter, HTTPException, status, Depends, Query, Header, Request
from src.services.payment_service import PaymentService
from src.middlewares.auth_middleware import get_current_user
from src.validators.payment_validator import CreateOrderRequest, VerifyPaymentRequest
from src.utils.response import success_response
from typing import Optional

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/webhook")
async def handle_webhook(request: Request, x_razorpay_signature: str = Header(None)):
    """Handle Razorpay webhook (no auth - Razorpay calls this)"""
    try:
        if not x_razorpay_signature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing signature"
            )

        payload = await request.json()
        result = await PaymentService.handleWebhook(payload, x_razorpay_signature)
        return success_response(result, "Webhook processed")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/create-order", status_code=status.HTTP_201_CREATED)
async def create_order(
    request: CreateOrderRequest, current_user: dict = Depends(get_current_user)
):
    """Create Razorpay order"""
    try:
        result = await PaymentService.createOrder(
            current_user["id"], request.amount, request.currency
        )
        return success_response(result, "Payment order created", status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/verify")
async def verify_payment(
    request: VerifyPaymentRequest, current_user: dict = Depends(get_current_user)
):
    """Verify payment"""
    try:
        payment = await PaymentService.verifyPayment(request.model_dump())
        return success_response(payment, "Payment verified successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/my-payments")
async def get_my_payments(
    limit: int = Query(default=50, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    current_user: dict = Depends(get_current_user),
):
    """Get user payments"""
    try:
        payments = await PaymentService.getPaymentsByUserId(
            current_user["id"], limit, offset
        )
        return success_response(payments, "Payments retrieved")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{payment_id}")
async def get_payment_by_id(
    payment_id: str, current_user: dict = Depends(get_current_user)
):
    """Get payment by ID"""
    try:
        payment = await PaymentService.getPaymentById(payment_id)

        # Verify ownership (unless admin)
        if payment["user_id"] != current_user["id"] and "admin" not in current_user.get(
            "roles", []
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized"
            )

        return success_response(payment, "Payment retrieved")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

