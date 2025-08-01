from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from src.db.entity import AnswerEntity, QuestionEntity, UserEntity


def get_question_list(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 10,
    keyword: str = "",
) -> tuple[int, list[QuestionEntity]]:
    # TODO. (refactoring) 함수 기능 분리
    question_list = db.query(QuestionEntity)
    if keyword:
        search = "%%{}%%".format(keyword)
        sub_query = (
            db.query(
                AnswerEntity.question_id,
                AnswerEntity.content,
                UserEntity.username,
            )
            .outerjoin(UserEntity, and_(AnswerEntity.user_id == UserEntity.id))
            .subquery()
        )
        question_list = (
            question_list.outerjoin(UserEntity)
            .outerjoin(sub_query, and_(sub_query.c.question_id == QuestionEntity.id))
            .filter(
                QuestionEntity.subject.ilike(search)  # 질문제목
                | QuestionEntity.content.ilike(search)  # 질문내용
                | UserEntity.username.ilike(search)  # 질문작성자
                | sub_query.c.content.ilike(search)  # 답변내용
                | sub_query.c.username.ilike(search)  # 답변작성자
            )
        )
    total = question_list.distinct().count()
    question_list = (
        question_list.order_by(QuestionEntity.create_date.desc())
        .offset(skip)
        .limit(limit)
        .distinct()
        .all()
    )
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)


def get_question(db: Session, *, question_id: int) -> QuestionEntity | None:
    question = db.query(QuestionEntity).get(question_id)
    return question
