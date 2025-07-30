import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from src.domain.answer.answer_model import AnswerResponse
from src.domain.user.user_model import User


class QuestionResponse(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    modify_date: datetime.datetime | None = None
    answers: list[AnswerResponse] = []
    user: User | None

    model_config = ConfigDict(from_attributes=True)


class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator("subject", "content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v


class QuestionList(BaseModel):
    total: int = 0
    question_list: list[QuestionResponse] = []


class QuestionUpdate(QuestionCreate):
    question_id: int


class QuestionDelete(BaseModel):
    question_id: int
