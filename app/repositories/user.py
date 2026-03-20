from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    @staticmethod
    def create(db: Session, payload: UserCreate) -> User:
        user = User(
            name=payload.name,
            email=payload.email,
            age=payload.age,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def list_users(db: Session, limit: int, offset: int) -> list[User]:
        stmt = select(User).offset(offset).limit(limit)
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def count(db: Session) -> int:
        stmt = select(func.count()).select_from(User)
        return db.execute(stmt).scalar_one()

    @staticmethod
    def update(db: Session, user: User, payload: UserUpdate) -> User:
        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user: User) -> None:
        db.delete(user)
        db.commit()
