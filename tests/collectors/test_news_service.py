from datetime import datetime, timedelta
from src.collectors.news_service import filter_yesterday, dedupe_news
from src.domain.news_entity import NewsItem


def test_filter_yesterday():
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    items = [
        NewsItem("A", "desc", "", "", yesterday),
        NewsItem("B", "desc", "", "", today),
    ]

    result = filter_yesterday(items)
    assert len(result) == 1
    assert result[0].title == "A"


def test_dedupe_news():
    items = [
        NewsItem("A", "hello world", "", "", datetime.now()),
        NewsItem("B", "hello wor1d", "", "", datetime.now()),
    ]

    result = dedupe_news(items, threshold=0.8)
    assert len(result) == 1
