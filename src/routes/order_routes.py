from fastapi import APIRouter, HTTPException, status, Depends, Query
from src.services.order_service import OrderService
from src.middlewares.auth_middleware import get_current_user
from src.validators.order_validator import (
    CreateOrderRequest,
    UpdateOrderStatusRequest,
)
from src.utils.response import success_response
from typing import Optional

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_order(
    request: CreateOrderRequest, current_user: dict = Depends(get_current_user)
):
    """Create order"""
    try:
        payment_id = str(request.paymentId) if request.paymentId else None
        order = await OrderService.createOrderRecord(
            current_user["id"], request.items, request.total, payment_id
        )
        return success_response(order, "Order created successfully", status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{order_id}")
async def get_order_by_id(
    order_id: str, current_user: dict = Depends(get_current_user)
):
    """Get order by ID"""
    try:
        user_id = None if "admin" in current_user.get("roles", []) else current_user["id"]
        order = await OrderService.getOrderById(order_id, user_id)
        return success_response(order, "Order retrieved")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("")
async def list_orders(
    limit: int = Query(default=50, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: dict = Depends(get_current_user),
):
    """List orders"""
    try:
        user_id = None if "admin" in current_user.get("roles", []) else current_user["id"]
        filters = {}
        if status_filter:
            filters["status"] = status_filter

        orders = await OrderService.listOrders(user_id, limit, offset, filters)
        return success_response(orders, "Orders retrieved")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: str,
    request: UpdateOrderStatusRequest,
    current_user: dict = Depends(get_current_user),
):
    """Update order status (admin or user for cancellation)"""
    try:
        # Users can only cancel their own orders
        user_id = None if "admin" in current_user.get("roles", []) else current_user["id"]
        if "admin" not in current_user.get("roles", []) and request.status != "cancelled":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can update order status",
            )

        order = await OrderService.updateOrderStatus(order_id, request.status, user_id)
        return success_response(order, "Order status updated")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

