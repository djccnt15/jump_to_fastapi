from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.db.database import get_db

from . import answer_service
from .answer_model import AnswerCreate

router = APIRouter(prefix="/answer")


@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(
    question_id: int,
    _answer_create: AnswerCreate,
    db: Session = Depends(get_db),
) -> None:
    answer_service.create_answer(question_id, _answer_create, db)
