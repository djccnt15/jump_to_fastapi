from sqlalchemy.orm import Session

from src.db.repository import question_repo

from .question_model import QuestionResponse


def get_question_list(db: Session):
    question_list = question_repo.get_question_list(db)
    return [QuestionResponse.model_validate(q) for q in question_list]


def get_question_detail(db: Session, id: int):
    question = question_repo.get_question(db, question_id=id)
    return QuestionResponse.model_validate(question)
