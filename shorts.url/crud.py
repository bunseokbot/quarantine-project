from random import choice
from sqlalchemy.orm import Session

from models import URL, History

import string


BASE_STRINGS = string.ascii_lowercase + string.ascii_uppercase + string.digits


def get_url_by_key(db: Session, key: str):
    return db.query(URL).filter(URL.key == key).first()


def create_url(db: Session, url: str):
    key = ''.join([choice(BASE_STRINGS) for _ in range(6)])
    db_url = URL(
        key=key,
        value=url,
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def create_history(db: Session, url_id: int):
    history = History(
        url_id=url_id,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history
