from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import BaseEntity

question_voter = Table(
    "question_voter",
    BaseEntity.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("question_id", Integer, ForeignKey("question.id"), primary_key=True),
)

answer_voter = Table(
    "answer_voter",
    BaseEntity.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("answer_id", Integer, ForeignKey("answer.id"), primary_key=True),
)


class QuestionEntity(BaseEntity):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    create_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    modify_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["UserEntity"] = relationship("UserEntity", backref="question_users")
    voter: Mapped[list["UserEntity"]] = relationship(
        "UserEntity",
        secondary=question_voter,
        backref="question_voters",
    )


class AnswerEntity(BaseEntity):
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    create_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("question.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    modify_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    question: Mapped["QuestionEntity"] = relationship(
        "QuestionEntity", backref="answers"
    )
    user: Mapped["UserEntity"] = relationship("UserEntity", backref="answer_users")
    voter: Mapped[list["UserEntity"]] = relationship(
        "UserEntity",
        secondary=answer_voter,
        backref="answer_voters",
    )


class UserEntity(BaseEntity):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
