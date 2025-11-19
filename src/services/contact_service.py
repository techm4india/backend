from src.utils.logger import log
from typing import Dict
from datetime import datetime


class ContactService:
    """Contact service for handling contact form submissions"""

    @staticmethod
    async def submitContactForm(data: Dict) -> Dict:
        """Submit contact form (can be extended to send email, save to DB, etc.)"""
        try:
            # Log the contact submission
            log(
                "INFO",
                "Contact form submission",
                {
                    "name": data.get("name"),
                    "email": data.get("email"),
                    "phone": data.get("phone"),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

            # TODO: Add functionality to:
            # 1. Save to database (create a contacts table)
            # 2. Send email notification
            # 3. Send confirmation email to user
            # 4. Integrate with email service (SendGrid, AWS SES, etc.)

            return {
                "id": f"contact_{int(datetime.utcnow().timestamp())}",
                "name": data.get("name"),
                "email": data.get("email"),
                "submitted_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            log("ERROR", "Contact form submission failed", {"error": str(e)})
            raise ValueError(f"Failed to submit contact form: {str(e)}")

