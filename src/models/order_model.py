from typing import Optional
from src.utils.logger import logger


class OrderModel:
    """Order model for Supabase operations"""

    @staticmethod
    async def create(order_data: dict) -> dict:
        """Create order record"""
        from src.config.supabase import supabase
        try:
            result = supabase.table("orders").insert(order_data).execute()
            if not result.data:
                raise ValueError("Failed to create order")
            return result.data[0]
        except Exception as e:
            logger.error("Error creating order", {"error": str(e)})
            raise

    @staticmethod
    async def findById(id: str) -> Optional[dict]:
        """Find order by ID"""
        from src.config.supabase import supabase
        try:
            result = (
                supabase.table("orders")
                .select("*, payments(*), users(id, email, name)")
                .eq("id", id)
                .execute()
            )
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error("Error finding order by id", {"error": str(e)})
            return None

    @staticmethod
    async def update(id: str, updates: dict) -> dict:
        """Update order"""
        from src.config.supabase import supabase
        try:
            result = (
                supabase.table("orders")
                .update(updates)
                .eq("id", id)
                .execute()
            )
            if not result.data:
                raise ValueError("Order not found or update failed")
            return result.data[0]
        except Exception as e:
            logger.error("Error updating order", {"error": str(e)})
            raise

    @staticmethod
    async def findByUserId(user_id: str, limit: int = 50, offset: int = 0) -> list:
        """Get orders by user ID"""
        from src.config.supabase import supabase
        try:
            result = (
                supabase.table("orders")
                .select("*, payments(*)")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            return result.data or []
        except Exception as e:
            logger.error("Error finding orders by user id", {"error": str(e)})
            raise

    @staticmethod
    async def list(limit: int = 100, offset: int = 0, filters: dict = None) -> list:
        """Get all orders (admin)"""
        from src.config.supabase import supabase
        try:
            query = (
                supabase.table("orders")
                .select("*, payments(*), users(id, email, name)")
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
            )
            
            if filters:
                if filters.get("status"):
                    query = query.eq("status", filters["status"])
                if filters.get("userId"):
                    query = query.eq("user_id", filters["userId"])
            
            result = query.execute()
            return result.data or []
        except Exception as e:
            logger.error("Error listing orders", {"error": str(e)})
            raise

