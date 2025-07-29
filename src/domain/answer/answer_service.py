from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db.entity import AnswerEntity, UserEntity
from src.db.repository import create_entity, question_repo

from .answer_model import AnswerCreate


def create_answer(
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
    create_entity(db, answer)
