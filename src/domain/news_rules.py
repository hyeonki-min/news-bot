from datetime import datetime, timedelta
from typing import List

from src.domain.news_entity import NewsItem


def yesterday_md() -> str:
    return (datetime.now() - timedelta(days=1)).strftime("%m%d%y")


def is_yesterday(dt: datetime) -> bool:
    now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
    yesterday = (now - timedelta(days=1)).date()
    return dt.date() == yesterday


def filter_yesterday(items: List[NewsItem]) -> List[NewsItem]:
    return [i for i in items if is_yesterday(i.pub_date)]


def jaccard_similarity(a: str, b: str) -> float:
    sa, sb = set(a), set(b)
    return len(sa & sb) / len(sa | sb) if sa | sb else 0


def dedupe_news(items: List[NewsItem], threshold: float = 0.8) -> List[NewsItem]:
    result = []
    for n in items:
        if not any(jaccard_similarity(n.description, r.description) > threshold for r in result):
            result.append(n)
    return result
