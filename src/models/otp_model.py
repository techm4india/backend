from typing import Optional
from datetime import datetime, timedelta
from src.utils.logger import logger


class OtpModel:
    """OTP model for Supabase operations"""

    @staticmethod
    async def create(otp_data: dict) -> dict:
        """Create OTP record"""
        from src.config.supabase import supabase
        try:
            result = supabase.table("otp_requests").insert(otp_data).execute()
            if not result.data:
                raise ValueError("Failed to create OTP")
            return result.data[0]
        except Exception as e:
            logger.error("Error creating OTP", {"error": str(e)})
            raise

    @staticmethod
    async def findValidOtp(target: str, code: str, type: str) -> Optional[dict]:
        """Find valid OTP by target and code"""
        from src.config.supabase import supabase
        try:
            now = datetime.utcnow().isoformat()
            result = (
                supabase.table("otp_requests")
                .select("*")
                .eq("target", target)
                .eq("code", code)
                .eq("type", type)
                .gt("expires_at", now)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error("Error finding OTP", {"error": str(e)})
            return None

    @staticmethod
    async def deleteExpired() -> bool:
        """Delete expired OTPs"""
        from src.config.supabase import supabase
        try:
            now = datetime.utcnow().isoformat()
            supabase.table("otp_requests").delete().lt("expires_at", now).execute()
            return True
        except Exception as e:
            logger.error("Error deleting expired OTPs", {"error": str(e)})
            raise

    @staticmethod
    async def delete(id: str) -> bool:
        """Delete OTP by ID"""
        from src.config.supabase import supabase
        try:
            supabase.table("otp_requests").delete().eq("id", id).execute()
            return True
        except Exception as e:
            logger.error("Error deleting OTP", {"error": str(e)})
            raise

    @staticmethod
    async def getRecentCount(target: str, minutes: int = 5) -> int:
        """Get recent OTP count for target (rate limiting)"""
        from src.config.supabase import supabase
        try:
            cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
            result = (
                supabase.table("otp_requests")
                .select("*", count="exact")
                .eq("target", target)
                .gte("created_at", cutoff_time.isoformat())
                .execute()
            )
            return result.count or 0
        except Exception as e:
            logger.error("Error getting recent OTP count", {"error": str(e)})
            return 0

