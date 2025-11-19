from pydantic import BaseModel, Field
from typing import Optional


class CreateOrderRequest(BaseModel):
    amount: float = Field(..., gt=0)
    currency: Optional[str] = Field(default="INR", pattern="^(INR|USD|EUR)$")


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str

