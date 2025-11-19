from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=1)
    phone: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SendOtpRequest(BaseModel):
    target: str = Field(..., min_length=1)
    type: Optional[str] = Field(default="register", pattern="^(login|register|reset)$")

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v not in ["login", "register", "reset"]:
            raise ValueError("Type must be login, register, or reset")
        return v


class VerifyOtpRequest(BaseModel):
    target: str = Field(..., min_length=1)
    code: str = Field(..., min_length=6, max_length=6, pattern="^[0-9]{6}$")
    type: Optional[str] = Field(default="register", pattern="^(login|register|reset)$")

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v not in ["login", "register", "reset"]:
            raise ValueError("Type must be login, register, or reset")
        return v


class RefreshTokenRequest(BaseModel):
    refreshToken: str

