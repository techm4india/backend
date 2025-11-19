from fastapi import APIRouter, HTTPException, status
from src.services.auth_service import AuthService
from src.validators.auth_validator import (
    RegisterRequest,
    LoginRequest,
    SendOtpRequest,
    VerifyOtpRequest,
    RefreshTokenRequest,
)
from src.utils.response import success_response, error_response

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """Register new user"""
    try:
        result = await AuthService.register(
            request.email, request.password, request.name, request.phone
        )
        return success_response(result, "User registered successfully", status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login")
async def login(request: LoginRequest):
    """Login user"""
    try:
        result = await AuthService.login(request.email, request.password)
        return success_response(result, "Login successful")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/send-otp")
async def send_otp(request: SendOtpRequest):
    """Send OTP"""
    try:
        result = await AuthService.sendOtp(request.target, request.type)
        return success_response(result, "OTP sent successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/verify-otp")
async def verify_otp(request: VerifyOtpRequest):
    """Verify OTP"""
    try:
        result = await AuthService.verifyOtp(request.target, request.code, request.type)
        return success_response(result, "OTP verified successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest):
    """Refresh token"""
    try:
        result = await AuthService.refreshToken(request.refreshToken)
        return success_response(result, "Token refreshed successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

