from src.models.order_model import OrderModel
from src.models.payment_model import PaymentModel


class OrderService:
    """Order service for order management"""

    @staticmethod
    async def createOrderRecord(
        user_id: str, items: list, total: float, payment_id: str = None
    ) -> dict:
        """Create order record"""
        if not items or not isinstance(items, list) or len(items) == 0:
            raise ValueError("Order must have at least one item")

        if not total or total <= 0:
            raise ValueError("Order total must be greater than 0")

        # If paymentId provided, verify it exists
        if payment_id:
            payment = await PaymentModel.findById(payment_id)
            if not payment:
                raise ValueError("Payment not found")
            if payment["user_id"] != user_id:
                raise ValueError("Payment does not belong to user")

        order = await OrderModel.create(
            {
                "user_id": user_id,
                "items": items,
                "total": total,
                "payment_id": payment_id,
                "status": "pending",
            }
        )

        return order

    @staticmethod
    async def getOrderById(id: str, user_id: str = None) -> dict:
        """Get order by ID"""
        order = await OrderModel.findById(id)

        if not order:
            raise ValueError("Order not found")

        # If userId provided, verify ownership
        if user_id and order["user_id"] != user_id:
            raise ValueError("Order not found")

        return order

    @staticmethod
    async def updateOrderStatus(
        id: str, status: str, user_id: str = None
    ) -> dict:
        """Update order status"""
        order = await OrderModel.findById(id)

        if not order:
            raise ValueError("Order not found")

        # If userId provided, verify ownership
        if user_id and order["user_id"] != user_id:
            raise ValueError("Unauthorized")

        valid_statuses = [
            "pending",
            "confirmed",
            "processing",
            "shipped",
            "delivered",
            "cancelled",
        ]
        if status not in valid_statuses:
            raise ValueError("Invalid order status")

        return await OrderModel.update(id, {"status": status})

    @staticmethod
    async def listOrders(
        user_id: str = None, limit: int = 50, offset: int = 0, filters: dict = None
    ) -> list:
        """List orders"""
        if user_id:
            # User's own orders
            return await OrderModel.findByUserId(user_id, limit, offset)
        else:
            # Admin: all orders
            return await OrderModel.list(limit, offset, filters or {})

