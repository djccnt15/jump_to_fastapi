from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.db.entity import AnswerEntity, UserEntity
from src.db.repository import answer_repo, delete_entity, question_repo, save_entity

from .answer_model import AnswerCreate, AnswerDelete, AnswerResponse, AnswerUpdate


def create_answer(
    *,
    question_id: int,
    answer_create: AnswerCreate,
    db: Session,
    user: UserEntity,
) -> None:
    # question 검증
    question = question_repo.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # answer 생성
    answer = AnswerEntity(
        question=question,
        content=answer_create.content,
        create_date=datetime.now(),
        user=user,
    )
    save_entity(db, answer)


def get_answer(*, db: Session, answer_id: int) -> AnswerResponse:
    answer = answer_repo.get_answer(db, answer_id=answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return AnswerResponse.model_validate(answer)


def update_answer(*, db: Session, answer_update: AnswerUpdate, user: UserEntity):
    answer_entity = answer_repo.get_answer(db, answer_id=answer_update.answer_id)
    if not answer_entity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="데이터를 찾을수 없습니다.",
        )
    if user.id != answer_entity.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="수정 권한이 없습니다.",
        )

    answer_entity.content = answer_update.content
    answer_entity.modify_date = datetime.now()
    save_entity(db, answer_entity)


def delete_answer(*, db: Session, answer_delete: AnswerDelete, user: UserEntity):
    db_answer = answer_repo.get_answer(db, answer_id=answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="데이터를 찾을수 없습니다.",
        )
    if user.id != db_answer.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="삭제 권한이 없습니다.",
        )
    delete_entity(db, db_answer)
