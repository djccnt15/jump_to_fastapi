from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.db.entity import QuestionEntity, UserEntity
from src.db.repository import delete_entity, question_repo, save_entity

from .question_model import (
    QuestionCreate,
    QuestionDelete,
    QuestionList,
    QuestionResponse,
    QuestionUpdate,
)


def get_question_list(*, db: Session, page: int, size: int) -> QuestionList:
    question_list = question_repo.get_question_list(db, skip=page * size, limit=size)
    # TODO. (refactoring) `get_question_list` 함수 리팩토링 후 코드 수정
    return QuestionList(
        total=question_list[0],
        question_list=[QuestionResponse.model_validate(q) for q in question_list[1]],
    )


def get_question_detail(*, db: Session, id: int):
    question = question_repo.get_question(db, question_id=id)
    return QuestionResponse.model_validate(question)


def create_question(*, db: Session, question_create: QuestionCreate, user: UserEntity):
    entity = QuestionEntity(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now(),
        user=user,
    )
    save_entity(db=db, entity=entity)


def update_question(db: Session, question_update: QuestionUpdate, user: UserEntity):
    question = question_repo.get_question(db, question_id=question_update.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="데이터를 찾을수 없습니다.",
        )
    if user.id != question.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="수정 권한이 없습니다.",
        )

    question.subject = question_update.subject
    question.content = question_update.content
    question.modify_date = datetime.now()
    save_entity(db, question)


def delete_question(db: Session, question_delete: QuestionDelete, user: UserEntity):
    question = question_repo.get_question(db, question_id=question_delete.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."
        )
    if user.id != question.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다."
        )
    delete_entity(db, question)
