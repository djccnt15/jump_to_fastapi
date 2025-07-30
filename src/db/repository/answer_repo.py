from sqlalchemy.orm import Session

from src.db.entity import AnswerEntity


def get_answer(db: Session, answer_id: int) -> AnswerEntity | None:
    return db.query(AnswerEntity).get(answer_id)
