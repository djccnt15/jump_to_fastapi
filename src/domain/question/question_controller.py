from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.db.database import get_db
from src.db.entity import UserEntity
from src.domain.user import user_service

from . import question_service
from .question_model import QuestionCreate, QuestionList, QuestionResponse

router = APIRouter(prefix="/question")


@router.get("/list")
def question_list(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 10,
) -> QuestionList:
    question_list = question_service.get_question_list(db, page=page, size=size)
    return question_list


@router.get("/detail/{question_id}")
def question_detail(
    question_id: int,
    db: Session = Depends(get_db),
) -> QuestionResponse:
    question = question_service.get_question_detail(db, question_id)
    return question


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(
    question_create: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(user_service.get_current_user),
) -> None:
    question_service.create_question(db, question_create, current_user)
