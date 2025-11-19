from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


class OrderItem(BaseModel):
    id: str
    name: Optional[str] = None
    quantity: int = Field(..., gt=0)
    price: float = Field(..., ge=0)


class CreateOrderRequest(BaseModel):
    items: List[OrderItem] = Field(..., min_length=1)
    total: float = Field(..., gt=0)
    paymentId: Optional[UUID] = None


class UpdateOrderStatusRequest(BaseModel):
    status: str = Field(..., pattern="^(pending|confirmed|processing|shipped|delivered|cancelled)$")

