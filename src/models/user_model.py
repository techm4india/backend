from typing import Optional
from src.config.supabase import supabase


class UserModel:
    """User model for Supabase operations"""

    @staticmethod
    async def create(user_data: dict) -> dict:
        """Create a new user"""
        try:
            result = supabase.table("users").insert(user_data).execute()
            if not result.data:
                raise ValueError("Failed to create user")
            return result.data[0]
        except Exception as e:
            from src.utils.logger import log
            log("ERROR", "Error creating user", {"error": str(e)})
            raise

    @staticmethod
    async def findByEmail(email: str) -> Optional[dict]:
        """Find user by email"""
        try:
            result = supabase.table("users").select("*").eq("email", email).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            from src.utils.logger import log
            log("ERROR", "Error finding user by email", {"error": str(e)})
            return None

    @staticmethod
    async def findById(id: str) -> Optional[dict]:
        """Find user by ID"""
        try:
            result = supabase.table("users").select("*").eq("id", id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            from src.utils.logger import log
            log("ERROR", "Error finding user by id", {"error": str(e)})
            return None

    @staticmethod
    async def findByPhone(phone: str) -> Optional[dict]:
        """Find user by phone"""
        try:
            result = supabase.table("users").select("*").eq("phone", phone).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            from src.utils.logger import log
            log("ERROR", "Error finding user by phone", {"error": str(e)})
            return None

    @staticmethod
    async def update(id: str, updates: dict) -> dict:
        """Update user"""
        try:
            result = (
                supabase.table("users")
                .update(updates)
                .eq("id", id)
                .execute()
            )
            if not result.data:
                raise ValueError("User not found or update failed")
            return result.data[0]
        except Exception as e:
            from src.utils.logger import log
            log("ERROR", "Error updating user", {"error": str(e)})
            raise

    @staticmethod
    async def verifyUser(id: str) -> dict:
        """Mark user as verified"""
        return await UserModel.update(id, {"is_verified": True})

    @staticmethod
    async def assignRole(id: str, role: str) -> dict:
        """Assign role to user"""
        user = await UserModel.findById(id)
        if not user:
            raise ValueError("User not found")
        
        roles = user.get("roles", []) or []
        if role not in roles:
            roles.append(role)
            return await UserModel.update(id, {"roles": roles})
        return user

    @staticmethod
    async def removeRole(id: str, role: str) -> dict:
        """Remove role from user"""
        user = await UserModel.findById(id)
        if not user:
            raise ValueError("User not found")
        
        roles = [r for r in (user.get("roles") or []) if r != role]
        return await UserModel.update(id, {"roles": roles})

    @staticmethod
    async def list(limit: int = 100, offset: int = 0) -> list:
        """List all users (admin)"""
        try:
            result = (
                supabase.table("users")
                .select("*")
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            return result.data or []
        except Exception as e:
            from src.utils.logger import log
            log("ERROR", "Error listing users", {"error": str(e)})
            raise

    @staticmethod
    async def delete(id: str) -> bool:
        """Delete user"""
        try:
            supabase.table("users").delete().eq("id", id).execute()
            return True
        except Exception as e:
            from src.utils.logger import log
            log("ERROR", "Error deleting user", {"error": str(e)})
            raise

