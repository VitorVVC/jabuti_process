from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import (
    PaginatedUsersResponse,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, payload)


@router.get("/", response_model=PaginatedUsersResponse)
def list_users(
        limit: int = Query(default=10, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
        db: Session = Depends(get_db),
):
    return UserService.list_users(db, limit, offset)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    return UserService.get_user_by_id(db, user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, payload: UserUpdate, db: Session = Depends(get_db)):
    return UserService.update_user(db, user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    UserService.delete_user(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
