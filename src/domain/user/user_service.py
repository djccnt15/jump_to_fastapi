from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status

from src import configuration
from src.configuration import pwd_context
from src.db.entity import UserEntity
from src.db.repository import create_entity, user_repo

from .user_model import Token, UserCreate


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


def create_user_token(form_data: OAuth2PasswordRequestForm, db: Session) -> Token:
    # check user and password
    user = user_repo.get_user(db, form_data.username)
    if not user or not configuration.pwd_context.verify(
        form_data.password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.username,
        "exp": datetime.utcnow()
        + timedelta(minutes=configuration.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(
        data,
        configuration.SECRET_KEY,
        algorithm=configuration.ALGORITHM,
    )

    return Token(access_token=access_token, token_type="bearer", username=user.username)
