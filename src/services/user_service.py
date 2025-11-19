from src.models.user_model import UserModel


class UserService:
    """User service for user management operations"""

    @staticmethod
    async def getUserById(id: str) -> dict:
        """Get user by ID"""
        user = await UserModel.findById(id)
        if not user:
            raise ValueError("User not found")

        # Remove sensitive data
        user.pop("password_hash", None)
        return user

    @staticmethod
    async def getMe(user_id: str) -> dict:
        """Get current user profile"""
        return await UserService.getUserById(user_id)

    @staticmethod
    async def updateMe(user_id: str, update_data: dict) -> dict:
        """Update current user profile"""
        # Remove fields that shouldn't be updated directly
        allowed_updates = {
            k: v
            for k, v in update_data.items()
            if k not in ["id", "email", "password_hash", "roles"]
        }

        user = await UserModel.update(user_id, allowed_updates)
        user.pop("password_hash", None)
        return user

    @staticmethod
    async def listUsers(limit: int = 100, offset: int = 0) -> list:
        """List all users (admin)"""
        users = await UserModel.list(limit, offset)
        # Remove password_hash from all users
        return [{k: v for k, v in user.items() if k != "password_hash"} for user in users]

    @staticmethod
    async def assignRole(user_id: str, role: str) -> dict:
        """Assign role to user (admin)"""
        user = await UserModel.assignRole(user_id, role)
        user.pop("password_hash", None)
        return user

    @staticmethod
    async def removeRole(user_id: str, role: str) -> dict:
        """Remove role from user (admin)"""
        user = await UserModel.removeRole(user_id, role)
        user.pop("password_hash", None)
        return user

