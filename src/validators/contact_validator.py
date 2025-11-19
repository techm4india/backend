from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ContactRequest(BaseModel):
    """Contact form request model"""
    name: str = Field(..., min_length=1, max_length=100, description="Contact name")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, max_length=20, description="Contact phone (optional)")
    message: str = Field(..., min_length=1, max_length=5000, description="Contact message")

