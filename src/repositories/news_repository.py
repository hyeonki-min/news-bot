from sqlalchemy.orm import Session
from src.domain.news_entity import NewsItem
from src.repositories.news_mapper import NewsMapper
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