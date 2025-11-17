from src.infra.embedding_client import EmbeddingClient
from src.domain.topic_classifier import classify_topic
from collections import defaultdict
from sqlalchemy.orm import Session
from src.repositories.news_repository import get_news_by_date
from src.app.schemas.news_dto import NewsDTO

client = EmbeddingClient()


def detect_topic(news):
    # news: NewsItem (domain entity)
    return classify_topic(news.description, client.embed, client.anchor_embeddings)

def group_by_topic_for_api(db: Session, date_str: str):
    items = get_news_by_date(db, date_str)

    result = defaultdict(list)
    for item in items:
        if item.topic and item.topic != "unknown":
            result[item.topic].append(NewsDTO.from_orm(item))

    return result