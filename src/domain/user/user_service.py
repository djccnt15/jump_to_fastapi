from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.configuration import pwd_context
from src.db.entity import UserEntity
from src.db.repository import create_entity, user_repo

from .user_model import UserCreate


def create_user(db: Session, user_create: UserCreate):
    user = user_repo.get_user_by_username_email(db, user_create)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 존재하는 사용자입니다.",
        )

    db_user = UserEntity(
        username=user_create.username,
        password=pwd_context.hash(user_create.password1),
        email=user_create.email,
    )
    create_entity(db, db_user)
