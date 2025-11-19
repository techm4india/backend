from fastapi import APIRouter
from src.routes.auth_routes import router as auth_router
from src.routes.user_routes import router as user_router
from src.routes.payment_routes import router as payment_router
from src.routes.order_routes import router as order_router
from src.routes.contact_routes import router as contact_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(payment_router)
api_router.include_router(order_router)
api_router.include_router(contact_router)

__all__ = ["api_router"]

