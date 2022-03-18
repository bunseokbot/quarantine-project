from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from datetime import datetime

from database import Base


class URL(Base):
    __tablename__ ="shorten_urls"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    user_agent = Column(String)
    remote_addr = Column(String)


class History(Base):
    __tablename__ = "url_redirect_histories"
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, default=datetime.utcnow)
    url_id = Column(Integer, ForeignKey("shorten_urls.id"))
    user_agent = Column(String)
    remote_addr = Column(String)
