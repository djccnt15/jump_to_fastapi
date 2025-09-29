import datetime

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User
from pydantic import BaseModel, ConfigDict, field_validator


class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    modify_date: datetime.datetime | None = None
    answers: list[Answer] = []
    user: User | None
    voter: list[User] = []


class QuestionV2(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    modify_date: datetime.datetime | None = None
    user: str | None
    voter: int | None
    answers: int | None

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
    question_list: list[Question] = []


class QuestionListV2(BaseModel):
    total: int = 0
    question_list: list[QuestionV2] = []


class QuestionUpdate(QuestionCreate):
    question_id: int


class QuestionDelete(BaseModel):
    question_id: int


class QuestionVote(BaseModel):
    question_id: int
