from sqlalchemy.orm import Session
from sqlalchemy import func
from src.domain.news_entity import NewsItem
from src.models.news_model import NewsItemModel
from src.repositories.news_mapper import NewsMapper
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


def save_news_bulk(db: Session, items: list[NewsItem]):
    logger.info(f"Saving {len(items)} news items into DB")
    try:
        models = [NewsMapper.to_model(item) for item in items]
        db.add_all(models)
        db.commit()
        logger.info("DB save commit successful")
    except Exception as ex:
        db.rollback()
        logger.exception("DB save failed, rollback executed")
        raise


def get_news_by_date(db: Session, date_str: str) -> list[NewsItemModel]:
    """
    YYYY-MM-DD 형태로 들어온 날짜 문자열 기준으로 뉴스 조회.
    """
    # 문자열을 date 형식으로 변환
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

    return (
        db.query(NewsItemModel)
        .filter(func.date(NewsItemModel.pub_date) == target_date)
        .order_by(NewsItemModel.pub_date.desc())
        .all()
    )