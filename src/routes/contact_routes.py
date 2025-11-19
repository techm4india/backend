from fastapi import APIRouter, HTTPException, status
from src.services.contact_service import ContactService
from src.validators.contact_validator import ContactRequest
from src.utils.response import success_response

router = APIRouter(prefix="/contact", tags=["Contact"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def submit_contact(request: ContactRequest):
    """Submit contact form"""
    try:
        result = await ContactService.submitContactForm(request.dict())
        return success_response(
            result,
            "Contact form submitted successfully",
            status.HTTP_201_CREATED
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/test")
async def test_contact_route():
    """Test endpoint to verify contact route is working"""
    return success_response(
        {"status": "working"},
        "Contact route is working!"
    )

