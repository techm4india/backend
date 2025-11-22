from src.models.user_model import UserModel
from src.services.otp_service import OtpService


class AuthService:
    """Authentication service using Supabase Auth"""

    @staticmethod
    async def register(email: str, password: str, name: str, phone: str = None) -> dict:
        """Register new user using Supabase Auth"""
        from src.config.supabase import supabase
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

    @staticmethod
    async def login(email: str, password: str) -> dict:
        """Login user using Supabase Auth"""
        from src.config.supabase import supabase
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

        return {
            "verified": True,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "phone": user.get("phone"),
                "is_verified": True,
            },
        }

    @staticmethod
    async def refreshToken(refresh_token: str) -> dict:
        """Refresh token using Supabase Auth"""
        from src.config.supabase import supabase
        try:
            result = supabase.auth.refresh_session(refresh_token)
            return {"session": result.session}
        except Exception as e:
            raise ValueError(f"Token refresh failed: {str(e)}")

