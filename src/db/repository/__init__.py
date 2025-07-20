from sqlalchemy.orm import DeclarativeBase, Session


def create_entity(db: Session, entity: DeclarativeBase):
    db.add(entity)
    db.commit()
