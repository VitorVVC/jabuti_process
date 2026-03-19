from uuid import uuid4

from fastapi import APIRouter, Query

from app.schemas.user import (
    PaginatedUsersResponse,
    UserCreate,
    UserResponse,
    UserUpdate,
)

router = APIRouter(prefix="/test_users", tags=["test_users"])


@router.get("/", response_model=PaginatedUsersResponse)
def list_users_test(
        limit: int = Query(default=10, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
):
    return PaginatedUsersResponse(
        items=[
            UserResponse(
                id=uuid4(),
                name="Vitor",
                email="vitor@email.com",
                age=19,
            )
        ],
        total=1,
        limit=limit,
        offset=offset,
    )


@router.post("/", response_model=UserResponse, status_code=201)
def create_user_test(payload: UserCreate):
    return UserResponse(
        id=uuid4(),
        name=payload.name,
        email=payload.email,
        age=payload.age,
    )


@router.put("/{user_id}", response_model=UserResponse)
def update_user_test(user_id: str, payload: UserUpdate):
    return UserResponse(
        id=uuid4(),
        name=payload.name or "Nome Atualizado",
        email=payload.email or "atualizado@email.com",
        age=payload.age if payload.age is not None else 20,
    )

