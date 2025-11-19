import pytest
from unittest.mock import AsyncMock, patch
from src.services.auth_service import AuthService
from src.models.user_model import UserModel


@pytest.mark.asyncio
async def test_register_custom_mode():
    """Test user registration in custom mode"""
    with patch("src.services.auth_service.AUTH_MODE", "custom"):
        with patch.object(UserModel, "findByEmail", return_value=None):
            with patch.object(
                UserModel,
                "create",
                return_value={
                    "id": "user-123",
                    "email": "test@example.com",
                    "name": "Test User",
                    "is_verified": False,
                },
            ):
                result = await AuthService.register(
                    "test@example.com", "password123", "Test User"
                )

                assert "user" in result
                assert "token" in result
                assert result["user"]["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_register_user_exists():
    """Test registration when user already exists"""
    with patch("src.services.auth_service.AUTH_MODE", "custom"):
        with patch.object(
            UserModel, "findByEmail", return_value={"id": "existing-user"}
        ):
            with pytest.raises(ValueError, match="User already exists"):
                await AuthService.register(
                    "test@example.com", "password123", "Test User"
                )


@pytest.mark.asyncio
async def test_login_custom_mode():
    """Test user login in custom mode"""
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("password123")

    with patch("src.services.auth_service.AUTH_MODE", "custom"):
        with patch.object(
            UserModel,
            "findByEmail",
            return_value={
                "id": "user-123",
                "email": "test@example.com",
                "password_hash": hashed_password,
                "name": "Test User",
                "is_verified": True,
                "roles": [],
            },
        ):
            result = await AuthService.login("test@example.com", "password123")

            assert "user" in result
            assert "token" in result
            assert result["user"]["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    with patch("src.services.auth_service.AUTH_MODE", "custom"):
        with patch.object(UserModel, "findByEmail", return_value=None):
            with pytest.raises(ValueError, match="Invalid credentials"):
                await AuthService.login("test@example.com", "wrongpassword")

