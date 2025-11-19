from typing import Optional
from src.config.supabase import supabase
from src.utils.logger import logger


class PaymentModel:
    """Payment model for Supabase operations"""

    @staticmethod
    async def create(payment_data: dict) -> dict:
        """Create payment record"""
        try:
            result = supabase.table("payments").insert(payment_data).execute()
            if not result.data:
                raise ValueError("Failed to create payment")
            return result.data[0]
        except Exception as e:
            logger.error("Error creating payment", {"error": str(e)})
            raise

    @staticmethod
    async def findById(id: str) -> Optional[dict]:
        """Find payment by ID"""
        try:
            result = supabase.table("payments").select("*").eq("id", id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error("Error finding payment by id", {"error": str(e)})
            return None

    @staticmethod
    async def findByProviderId(provider_payment_id: str) -> Optional[dict]:
        """Find payment by provider payment ID"""
        try:
            result = (
                supabase.table("payments")
                .select("*")
                .eq("provider_payment_id", provider_payment_id)
                .execute()
            )
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error("Error finding payment by provider id", {"error": str(e)})
            return None

    @staticmethod
    async def update(id: str, updates: dict) -> dict:
        """Update payment"""
        try:
            result = (
                supabase.table("payments")
                .update(updates)
                .eq("id", id)
                .execute()
            )
            if not result.data:
                raise ValueError("Payment not found or update failed")
            return result.data[0]
        except Exception as e:
            logger.error("Error updating payment", {"error": str(e)})
            raise

    @staticmethod
    async def findByUserId(user_id: str, limit: int = 50, offset: int = 0) -> list:
        """Get payments by user ID"""
        try:
            result = (
                supabase.table("payments")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            return result.data or []
        except Exception as e:
            logger.error("Error finding payments by user id", {"error": str(e)})
            raise

    @staticmethod
    async def list(limit: int = 100, offset: int = 0) -> list:
        """Get all payments (admin)"""
        try:
            result = (
                supabase.table("payments")
                .select("*")
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            return result.data or []
        except Exception as e:
            logger.error("Error listing payments", {"error": str(e)})
            raise

