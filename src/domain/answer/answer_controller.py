from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.db.database import get_db
from src.db.entity import UserEntity
from src.domain.user import user_service

from . import answer_service
from .answer_model import AnswerCreate, AnswerDelete, AnswerResponse, AnswerUpdate

router = APIRouter(prefix="/answer")


@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(
    question_id: int,
    _answer_create: AnswerCreate,
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(user_service.get_current_user),
) -> None:
    answer_service.create_answer(
        question_id=question_id,
        answer_create=_answer_create,
        db=db,
        user=current_user,
    )


@router.get("/detail/{answer_id}")
def answer_detail(answer_id: int, db: Session = Depends(get_db)) -> AnswerResponse:
    return answer_service.get_answer(db=db, answer_id=answer_id)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(
    _answer_update: AnswerUpdate,
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(user_service.get_current_user),
) -> None:
    answer_service.update_answer(db=db, answer_update=_answer_update, user=current_user)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(
    _answer_delete: AnswerDelete,
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(user_service.get_current_user),
) -> None:
    answer_service.delete_answer(db=db, answer_delete=_answer_delete, user=current_user)
