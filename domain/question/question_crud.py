from datetime import datetime

from domain.question.question_schema import QuestionCreate, QuestionUpdate
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.sql import and_, text

from models import Answer, Question, User

from .question_schema import QuestionV2


def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ""):
    question_list = db.query(Question)
    if keyword:
        search = "%%{}%%".format(keyword)
        sub_query = (
            db.query(Answer.question_id, Answer.content, User.username)
            .outerjoin(User, and_(Answer.user_id == User.id))
            .subquery()
        )
        question_list = (
            question_list.outerjoin(User)
            .outerjoin(sub_query, and_(sub_query.c.question_id == Question.id))
            .filter(
                Question.subject.ilike(search)  # 질문제목
                | Question.content.ilike(search)  # 질문내용
                | User.username.ilike(search)  # 질문작성자
                | sub_query.c.content.ilike(search)  # 답변내용
                | sub_query.c.username.ilike(search)  # 답변작성자
            )
        )
    total = question_list.distinct().count()
    question_list = (
        question_list.order_by(Question.create_date.desc())
        .offset(skip)
        .limit(limit)
        .distinct()
        .all()
    )
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)


def get_question_list_v2(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 10,
    keyword: str = "",
) -> tuple[int, list[Question]]:
    # TODO. (refactoring) 함수 기능 분리
    question_list = db.query(Question)
    if keyword:
        search = "%%{}%%".format(keyword)
        sub_query = (
            db.query(
                Answer.question_id,
                Answer.content,
                User.username,
            )
            .outerjoin(User, Answer.user_id == User.id)
            .subquery()
        )
        question_list = (
            question_list.outerjoin(User)
            .outerjoin(sub_query, sub_query.c.question_id == Question.id)
            .filter(
                Question.subject.ilike(search)  # 질문제목
                | Question.content.ilike(search)  # 질문내용
                | User.username.ilike(search)  # 질문작성자
                | sub_query.c.content.ilike(search)  # 답변내용
                | sub_query.c.username.ilike(search)  # 답변작성자
            )
        )
    total = question_list.distinct().count()
    question_list = (
        question_list.options(
            # question author
            selectinload(Question.user),
            # question voters
            selectinload(Question.voter),
            # answer author
            selectinload(Question.answers).selectinload(Answer.user),
            # answer voters
            selectinload(Question.answers).selectinload(Answer.voter),
        )
        .order_by(Question.create_date.desc())
        .offset(skip)
        .limit(limit)
        .distinct()
        .all()
    )
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)


def get_question_list_v3(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 10,
    keyword: str = "",
) -> list[QuestionV2]:
    stmt = """
WITH question_votes AS (
    SELECT question_id, COUNT(*) AS qv_count
    FROM question_voter qv
    GROUP BY question_id
),
answer_counts AS (
    SELECT a.question_id, COUNT(*) AS a_count
    FROM answer a
    GROUP BY a.question_id
)
SELECT DISTINCT
    q.id
    , q.subject
    , q.content
    , q.create_date
    , q.modify_date
    , qu.username AS user
    , qv_count AS voter
    , a_count AS answers
FROM question q
LEFT JOIN "user" qu ON qu.id = q.user_id
LEFT JOIN answer a ON a.question_id = q.id
LEFT JOIN "user" au ON a.user_id = au.id
LEFT JOIN question_votes ON question_votes.question_id = q.id
LEFT JOIN answer_counts ON answer_counts.question_id = q.id
WHERE :kw IS NULL
    OR q.subject LIKE :kw
    OR q.content LIKE :kw
    OR qu.username LIKE :kw
    OR a.content LIKE :kw
    OR au.username LIKE :kw
ORDER BY q.id DESC
LIMIT :rows OFFSET :page
;
"""
    params = {"kw": f"%{keyword}%" if keyword else None, "rows": limit, "page": skip}
    res = db.execute(text(stmt), params=params)
    question_list = [
        QuestionV2.model_validate(dict(zip(res.keys(), row))) for row in res.all()
    ]
    return question_list


def get_question_count_v3(
    db: Session,
    *,
    keyword: str = "",
) -> int:
    stmt = """
SELECT COUNT(DISTINCT q.id) AS total
FROM question q
LEFT JOIN "user" qu ON qu.id = q.user_id
LEFT JOIN answer a ON a.question_id = q.id
LEFT JOIN "user" au ON a.user_id = au.id
WHERE :kw IS NULL
    OR q.subject LIKE :kw
    OR q.content LIKE :kw
    OR qu.username LIKE :kw
    OR a.content LIKE :kw
    OR au.username LIKE :kw
;
"""
    params = {"kw": f"%{keyword}%" if keyword else None}
    res = db.execute(text(stmt), params=params)
    return res.scalar_one()


def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question


def create_question(db: Session, question_create: QuestionCreate, user: User):
    db_question = Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now(),
        user=user,
    )
    db.add(db_question)
    db.commit()


def update_question(
    db: Session,
    db_question: Question,
    question_update: QuestionUpdate,
):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()


def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()


def vote_question(db: Session, db_question: Question, db_user: User):
    db_question.voter.append(db_user)
    db.commit()
