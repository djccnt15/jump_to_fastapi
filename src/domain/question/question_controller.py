from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.db.database import get_db
from src.db.entity import UserEntity
from src.domain.user import user_service

from . import question_service
from .question_model import (
    QuestionCreate,
    QuestionDelete,
    QuestionList,
    QuestionResponse,
    QuestionUpdate,
    QuestionVote,
)

router = APIRouter(prefix="/question")


@router.get("/list")
def question_list(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 10,
) -> QuestionList:
    question_list = question_service.get_question_list(db=db, page=page, size=size)
    return question_list


@router.get("/detail/{question_id}")
def question_detail(
    question_id: int,
    db: Session = Depends(get_db),
) -> QuestionResponse:
    question = question_service.get_question_detail(db=db, id=question_id)
    return question


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(
    question_create: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(user_service.get_current_user),
) -> None:
    question_service.create_question(
        db=db,
        question_create=question_create,
        user=current_user,
    )


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(
    _question_update: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(user_service.get_current_user),
) -> None:
    question_service.update_question(db, _question_update, current_user)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(
    _question_delete: QuestionDelete,
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(user_service.get_current_user),
) -> None:
    question_service.delete_question(db, _question_delete, current_user)


@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def question_vote(
    _question_vote: QuestionVote,
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(user_service.get_current_user),
) -> None:
    question_service.vote_question(
        question_vote=_question_vote, db=db, user=current_user
    )
