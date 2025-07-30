from sqlalchemy.orm import DeclarativeBase, Session


def save_entity(db: Session, entity: DeclarativeBase):
    db.add(entity)
    db.commit()


def delete_entity(db: Session, entity: DeclarativeBase):
    db.delete(entity)
    db.commit()
