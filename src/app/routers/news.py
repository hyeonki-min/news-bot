from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.infra.db import get_db
from src.services.topic_service import group_by_topic_for_api
from datetime import date

router = APIRouter()


@router.get("/news")
def get_news(
    date: str = Query(default=date.today().strftime("%Y-%m-%d"), description="YYYY-MM-DD 형식 날짜"),
    db: Session = Depends(get_db)
):
    """
    지정된 날짜의 뉴스를 반환한다.
    /news?date=2025-01-10
    """
    try:
        return group_by_topic_for_api(db, date)
    except ValueError as e:
        return {"error": str(e)}
