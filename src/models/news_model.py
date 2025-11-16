from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.core.db import Base

class NewsItemModel(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    link = Column(String)
    original_link = Column(String)
    pub_date = Column(DateTime)
    topic = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
