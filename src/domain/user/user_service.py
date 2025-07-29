from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from src import configuration
from src.configuration import pwd_context
from src.db.database import get_db
from src.db.entity import UserEntity
from src.db.repository import create_entity, user_repo

from .user_model import Token, TokenData, UserCreate


def create_user(db: Session, user_create: UserCreate):
    user = user_repo.get_user_by_username_email(db, user_create=user_create)
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
    user = user_repo.get_user(db, username=form_data.username)
    if not user or not configuration.pwd_context.verify(
        form_data.password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = TokenData(
        sub=user.username,
        exp=datetime.utcnow()
        + timedelta(minutes=configuration.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    access_token = jwt.encode(
        vars(data),
        configuration.SECRET_KEY,
        algorithm=configuration.ALGORITHM,
    )

    return Token(access_token=access_token, token_type="bearer", username=user.username)


def get_current_user(
    token: str = Depends(configuration.oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = TokenData.model_validate(
            jwt.decode(
                token,
                configuration.SECRET_KEY,
                algorithms=[configuration.ALGORITHM],
            )
        )
        username: str = payload.sub
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_repo.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user
