from fastapi import APIRouter, HTTPException, status, Depends, Query
from src.services.user_service import UserService
from src.middlewares.auth_middleware import get_current_user, get_current_admin_user
from src.validators.auth_validator import RegisterRequest  # For update, we'll use a simple dict
from src.utils.response import success_response
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None


class AssignRoleRequest(BaseModel):
    role: str


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    try:
        user = await UserService.getMe(current_user["id"])
        return success_response(user, "User profile retrieved")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/me")
async def update_me(
    request: UpdateUserRequest, current_user: dict = Depends(get_current_user)
):
    """Update current user profile"""
    try:
        update_data = request.model_dump(exclude_unset=True)
        user = await UserService.updateMe(current_user["id"], update_data)
        return success_response(user, "Profile updated successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: str, current_user: dict = Depends(get_current_admin_user)
):
    """Get user by ID (admin)"""
    try:
        user = await UserService.getUserById(user_id)
        return success_response(user, "User retrieved")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("")
async def list_users(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    current_user: dict = Depends(get_current_admin_user),
):
    """List all users (admin)"""
    try:
        users = await UserService.listUsers(limit, offset)
        return success_response(users, "Users retrieved")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{user_id}/assign-role")
async def assign_role(
    user_id: str,
    request: AssignRoleRequest,
    current_user: dict = Depends(get_current_admin_user),
):
    """Assign role to user (admin)"""
    try:
        user = await UserService.assignRole(user_id, request.role)
        return success_response(user, "Role assigned successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{user_id}/remove-role")
async def remove_role(
    user_id: str,
    request: AssignRoleRequest,
    current_user: dict = Depends(get_current_admin_user),
):
    """Remove role from user (admin)"""
    try:
        user = await UserService.removeRole(user_id, request.role)
        return success_response(user, "Role removed successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

