import random
from datetime import datetime, timedelta
from src.models.otp_model import OtpModel
from src.utils.logger import logger


class OtpService:
    """OTP service for generating and verifying OTPs"""

    @staticmethod
    def generateOtp() -> str:
        """Generate 6-digit OTP"""
        return str(random.randint(100000, 999999))

    @staticmethod
    async def createOtp(target: str, type: str = "register") -> dict:
        """Create OTP and send (mock - integrate with SMS/Email service)"""
        # Rate limiting: max 3 OTPs per 5 minutes
        recent_count = await OtpModel.getRecentCount(target, 5)
        if recent_count >= 3:
            raise ValueError("Too many OTP requests. Please wait before requesting again.")

        code = OtpService.generateOtp()
        expires_at = datetime.utcnow() + timedelta(minutes=5)  # 5 minutes expiry

        otp_data = {
            "target": target,
            "code": code,
            "type": type,
            "expires_at": expires_at.isoformat(),
        }

        otp = await OtpModel.create(otp_data)

        # TODO: Integrate with SMS/Email service to send OTP
        # For now, log it (remove in production)
        from src.utils.logger import log
        log("INFO", f"OTP for {target}: {code} (expires in 5 minutes)")

        return {
            "id": otp["id"],
            "target": otp["target"],
            "expires_at": otp["expires_at"],
            # Don't return code in production
        }

    @staticmethod
    async def verifyOtp(target: str, code: str, type: str = "register") -> dict:
        """Verify OTP"""
        otp = await OtpModel.findValidOtp(target, code, type)

        if not otp:
            raise ValueError("Invalid or expired OTP")

        # Delete used OTP
        await OtpModel.delete(otp["id"])

        return {
            "valid": True,
            "target": otp["target"],
            "type": otp["type"],
        }

