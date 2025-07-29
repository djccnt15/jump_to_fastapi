from datetime import datetime

from sqlalchemy.orm import Session

from src.db.entity import QuestionEntity, UserEntity
from src.db.repository import create_entity, question_repo

from .question_model import QuestionCreate, QuestionList, QuestionResponse


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
    create_entity(db=db, entity=entity)
