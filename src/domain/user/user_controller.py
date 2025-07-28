from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from src.db.database import get_db

from . import user_model, user_service

router = APIRouter(prefix="/user")


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(
    _user_create: user_model.UserCreate,
    db: Session = Depends(get_db),
) -> None:
    user_service.create_user(db, _user_create)


@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> user_model.Token:
    return user_service.create_user_token(form_data, db)
