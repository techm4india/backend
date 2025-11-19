import os
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.config.supabase import supabase
from src.models.user_model import UserModel
from src.utils.jwt import verify_token
from dotenv import load_dotenv

load_dotenv()

AUTH_MODE = os.getenv("AUTH_MODE", "custom")
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Authentication dependency - supports both Supabase Auth and Custom JWT"""
    token = credentials.credentials
    user = None

    try:
        if AUTH_MODE == "supabase":
            # Verify Supabase JWT
            result = supabase.auth.get_user(token)

            if not result.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                )

            # Get user from our users table
            user = await UserModel.findByEmail(result.user.email)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                )
        else:
            # Verify custom JWT
            decoded = verify_token(token)

            # Get user from database
            user = await UserModel.findById(decoded["id"])
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                )

        # Return user data
        return {
            "id": user["id"],
            "email": user["email"],
            "name": user.get("name"),
            "phone": user.get("phone"),
            "roles": user.get("roles", []),
            "is_verified": user.get("is_verified", False),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
        )


async def get_current_admin_user(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Admin-only dependency"""
    if "admin" not in current_user.get("roles", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return current_user

