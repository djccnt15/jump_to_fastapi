from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.database import get_db

from . import question_service
from .question_model import QuestionResponse

router = APIRouter(prefix="/question")


@router.get("/list")
def question_list(db: Session = Depends(get_db)) -> list[QuestionResponse]:
    _question_list = question_service.get_question_list(db)
    return _question_list


@router.get("/detail/{question_id}")
def question_detail(
    question_id: int,
    db: Session = Depends(get_db),
) -> QuestionResponse:
    question = question_service.get_question_detail(db, question_id)
    return question
