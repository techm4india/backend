import os
from passlib.context import CryptContext
from src.config.supabase import supabase
from src.models.user_model import UserModel
from src.services.otp_service import OtpService
from src.utils.jwt import generate_token
from dotenv import load_dotenv

load_dotenv()

AUTH_MODE = os.getenv("AUTH_MODE", "custom")
BCRYPT_SALT_ROUNDS = int(os.getenv("BCRYPT_SALT_ROUNDS", "10"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service supporting both Supabase Auth and Custom JWT"""

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def register(email: str, password: str, name: str, phone: str = None) -> dict:
        """Register new user"""
        if AUTH_MODE == "supabase":
            # Use Supabase Auth
            try:
                result = supabase.auth.sign_up(
                    {
                        "email": email,
                        "password": password,
                        "options": {
                            "data": {
                                "name": name,
                                "phone": phone,
                            }
                        },
                    }
                )

                if result.user is None:
                    raise ValueError("Failed to create user in Supabase Auth")

                # Get user from our users table (if auto-created via trigger) or create manually
                user = await UserModel.findByEmail(email)
                if not user:
                    # Create user record in our users table
                    user = await UserModel.create(
                        {
                            "email": email,
                            "name": name,
                            "phone": phone,
                            "is_verified": False,
                        }
                    )

                return {
                    "user": {
                        "id": user["id"],
                        "email": user["email"],
                        "name": user["name"],
                        "phone": user.get("phone"),
                        "is_verified": user.get("is_verified", False),
                    },
                    "session": result.session,
                }
            except Exception as e:
                raise ValueError(f"Registration failed: {str(e)}")
        else:
            # Custom JWT auth
            # Check if user exists
            existing_user = await UserModel.findByEmail(email)
            if existing_user:
                raise ValueError("User already exists")

            # Hash password
            password_hash = AuthService._hash_password(password)

            # Create user
            user = await UserModel.create(
                {
                    "email": email,
                    "password_hash": password_hash,
                    "name": name,
                    "phone": phone,
                    "is_verified": False,
                }
            )

            # Generate JWT
            token = generate_token({"id": user["id"], "email": user["email"]})

            return {
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "name": user["name"],
                    "phone": user.get("phone"),
                    "is_verified": user.get("is_verified", False),
                },
                "token": token,
            }

    @staticmethod
    async def login(email: str, password: str) -> dict:
        """Login user"""
        if AUTH_MODE == "supabase":
            # Use Supabase Auth
            try:
                result = supabase.auth.sign_in_with_password(
                    {"email": email, "password": password}
                )

                if result.user is None:
                    raise ValueError("Invalid credentials")

                # Get user from our users table
                user = await UserModel.findByEmail(email)
                if not user:
                    raise ValueError("User not found in database")

                return {
                    "user": {
                        "id": user["id"],
                        "email": user["email"],
                        "name": user["name"],
                        "phone": user.get("phone"),
                        "is_verified": user.get("is_verified", False),
                        "roles": user.get("roles", []),
                    },
                    "session": result.session,
                }
            except Exception as e:
                raise ValueError(f"Login failed: {str(e)}")
        else:
            # Custom JWT auth
            user = await UserModel.findByEmail(email)
            if not user or not user.get("password_hash"):
                raise ValueError("Invalid credentials")

            # Verify password
            if not AuthService._verify_password(password, user["password_hash"]):
                raise ValueError("Invalid credentials")

            # Generate JWT
            token = generate_token({"id": user["id"], "email": user["email"]})

            return {
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "name": user["name"],
                    "phone": user.get("phone"),
                    "is_verified": user.get("is_verified", False),
                    "roles": user.get("roles", []),
                },
                "token": token,
            }

    @staticmethod
    async def sendOtp(target: str, type: str = "register") -> dict:
        """Send OTP"""
        return await OtpService.createOtp(target, type)

    @staticmethod
    async def verifyOtp(target: str, code: str, type: str = "register") -> dict:
        """Verify OTP and mark user as verified"""
        # Verify OTP
        verification = await OtpService.verifyOtp(target, code, type)

        # Find user by email or phone
        user = await UserModel.findByEmail(target)
        if not user:
            user = await UserModel.findByPhone(target)

        if not user:
            raise ValueError("User not found")

        # Mark user as verified
        await UserModel.verifyUser(user["id"])

        # Generate token
        token = None
        if AUTH_MODE == "custom":
            token = generate_token({"id": user["id"], "email": user["email"]})

        return {
            "verified": True,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "phone": user.get("phone"),
                "is_verified": True,
            },
            **({"token": token} if token else {}),
        }

    @staticmethod
    async def refreshToken(refresh_token: str) -> dict:
        """Refresh token (for Supabase Auth)"""
        if AUTH_MODE != "supabase":
            raise ValueError("Refresh token only available in Supabase auth mode")

        try:
            result = supabase.auth.refresh_session(refresh_token)
            return {"session": result.session}
        except Exception as e:
            raise ValueError(f"Token refresh failed: {str(e)}")

