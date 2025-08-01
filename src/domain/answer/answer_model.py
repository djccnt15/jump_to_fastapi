import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from src.domain.user.user_model import User


class AnswerCreate(BaseModel):
    content: str

    @field_validator("content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v


class AnswerResponse(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    question_id: int
    modify_date: datetime.datetime | None = None
    user: User | None
    voter: list[User] = []

    model_config = ConfigDict(from_attributes=True)


class AnswerUpdate(AnswerCreate):
    answer_id: int


class AnswerDelete(BaseModel):
    answer_id: int


class AnswerVote(BaseModel):
    answer_id: int
