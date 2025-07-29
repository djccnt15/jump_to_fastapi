from sqlalchemy.orm import Session

from src.db.entity import UserEntity
from src.domain.user.user_model import UserCreate


def get_user_by_username_email(db: Session, *, user_create: UserCreate):
    return (
        db.query(UserEntity)
        .filter(
            (UserEntity.username == user_create.username)
            | (UserEntity.email == user_create.email)
        )
        .first()
    )


def get_user(db: Session, *, username: str):
    return db.query(UserEntity).filter(UserEntity.username == username).first()
