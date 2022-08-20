from sqlalchemy.orm import Session

from .secret import get_db_secret


def init_db_from_secrets():
    init_db(
        user=get_db_secret()['username'],
        password=get_db_secret()['password'],
        host=get_db_secret()['host'],
        database=get_db_secret()['database'],
    )


def get_or_create(db: Session, model, **kwargs):
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance
