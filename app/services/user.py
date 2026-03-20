from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.cache.redis_client import RedisCache
from app.repositories.user import UserRepository
from app.schemas.user import (
    PaginatedUsersResponse,
    UserCreate,
    UserResponse,
    UserUpdate,
)


class UserService:
    @staticmethod
    def create_user(db: Session, payload: UserCreate) -> UserResponse:
        existing_user = UserRepository.get_by_email(db, payload.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists."
            )

        user = UserRepository.create(db, payload)

        RedisCache.delete_by_pattern("users:list:*")

        return UserResponse.model_validate(user)

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> UserResponse:
        cache_key = f"user:{user_id}"
        cached_user = RedisCache.get(cache_key)

        if cached_user:
            return UserResponse(**cached_user)

        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        user_response = UserResponse.model_validate(user)
        RedisCache.set(cache_key, user_response.model_dump(mode="json"))

        return user_response

    @staticmethod
    def list_users(db: Session, limit: int, offset: int) -> PaginatedUsersResponse:
        cache_key = f"users:list:{limit}:{offset}"
        cached_users = RedisCache.get(cache_key)

        if cached_users:
            return PaginatedUsersResponse(**cached_users)

        users = UserRepository.list_users(db, limit, offset)
        total = UserRepository.count(db)

        response = PaginatedUsersResponse(
            items=[UserResponse.model_validate(user) for user in users],
            total=total,
            limit=limit,
            offset=offset,
        )

        RedisCache.set(cache_key, response.model_dump(mode="json"))

        return response

    @staticmethod
    def update_user(db: Session, user_id: UUID, payload: UserUpdate) -> UserResponse:
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        if payload.email is not None and payload.email != user.email:
            existing_user = UserRepository.get_by_email(db, payload.email)

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists."
                )

        updated_user = UserRepository.update(db, user, payload)

        RedisCache.delete(f"user:{user_id}")
        RedisCache.delete_by_pattern("users:list:*")

        return UserResponse.model_validate(updated_user)

    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> None:
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        UserRepository.delete(db, user)

        RedisCache.delete(f"user:{user_id}")
        RedisCache.delete_by_pattern("users:list:*")
