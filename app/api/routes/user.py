from uuid import uuid4

from fastapi import APIRouter

from app.schemas.user import UserResponse, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def list_users_placeholder():
    return {"message": "users endpoint ok"}

