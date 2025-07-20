from typing import List

from sqlalchemy.orm import Session

from src.db.entity import QuestionEntity


def get_question_list(db: Session) -> List[QuestionEntity]:
    question_list = (
        db.query(QuestionEntity).order_by(QuestionEntity.create_date.desc()).all()
    )
    return question_list


def get_question(db: Session, question_id: int) -> QuestionEntity | None:
    question = db.query(QuestionEntity).get(question_id)
    return question
