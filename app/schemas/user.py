from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        example="John Dee"
    )
    email: EmailStr = Field(
        ...,
        example="example@gmail.com"
    )
    age: int = Field(
        ...,
        ge=0,
        le=150,
        example=33
    )


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
        example="New Name"
    )
    email: Optional[EmailStr] = Field(
        default=None,
        example="new_example@gmail.com"
    )
    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=150,
        example=34
    )


class UserResponse(UserBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class PaginatedUsersResponse(BaseModel):
    items: list[UserResponse]
    total: int
    limit: int
    offset: int
