from sqlalchemy.orm import Session

from src.db.entity import QuestionEntity


def get_question_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
) -> tuple[int, list[QuestionEntity]]:
    # TODO. (refactoring) 함수 기능 분리
    question_list = db.query(QuestionEntity).order_by(QuestionEntity.create_date.desc())
    total = question_list.count()
    question_list = question_list.offset(skip).limit(limit).all()
    return total, question_list


def get_question(db: Session, question_id: int) -> QuestionEntity | None:
    question = db.query(QuestionEntity).get(question_id)
    return question
