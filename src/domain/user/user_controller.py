from fastapi import APIRouter, Depends
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
