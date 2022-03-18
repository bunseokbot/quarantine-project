from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from crud import get_url_by_key, create_history, create_url
from models import Base, URL
from database import SessionLocal, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()


class Item(BaseModel):
    url: str


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register")
def register_new_url(item: Item, db: Session = Depends(get_database)):
    url = create_url(db, item.url)
    return {
        'short': url.key
    }


@app.get("/{url_id}")
def redirect_url_id(url_id: str, db: Session = Depends(get_database)):
    if len(url_id) != 6:
        raise HTTPException(status_code=400, detail="Invalid URL ID value")

    url: Optional[URL] = get_url_by_key(db, url_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL ID not found")

    if not url.is_active:
        raise HTTPException(status_code=403, detail="Forbidden by admin")

    create_history(db, url.id)
    return RedirectResponse(url.value)


@app.get("/")
def index():
    return {
        'msg': 'Hello?'
    }
