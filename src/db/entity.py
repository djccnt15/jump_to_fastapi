from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import BaseEntity


class QuestionEntity(BaseEntity):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    create_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    modify_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["UserEntity"] = relationship("UserEntity", backref="question_users")


class AnswerEntity(BaseEntity):
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    create_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("question.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    modify_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    question: Mapped[QuestionEntity] = relationship("QuestionEntity", backref="answers")
    user: Mapped["UserEntity"] = relationship("UserEntity", backref="answer_users")


class UserEntity(BaseEntity):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
