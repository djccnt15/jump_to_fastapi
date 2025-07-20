import datetime

from pydantic import BaseModel, ConfigDict

from src.domain.answer.answer_model import AnswerResponse


class QuestionResponse(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[AnswerResponse] = []

    model_config = ConfigDict(from_attributes=True)
