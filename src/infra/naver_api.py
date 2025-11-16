import requests
from datetime import datetime
from typing import List

from src.domain.news_entity import NewsItem
from src.utils import clean_html, parse_rfc822
import logging
logger = logging.getLogger(__name__)


def fetch_news(query: str, client_id: str, secret: str) -> List[NewsItem]:
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": secret,
    }

    params = {"query": query, "display": 100, "start": 1, "sort": "date"}

    try:
        resp = requests.get(
            "https://openapi.naver.com/v1/search/news.json",
            headers=headers,
            params=params,
        )
        resp.raise_for_status()

        data = resp.json()
        items = data.get("items", [])

        return [
            NewsItem(
                title=clean_html(i["title"]),
                description=clean_html(i["description"]),
                link=i.get("link", ""),
                original_link=i.get("originallink", ""),
                pub_date=parse_rfc822(i["pubDate"]),
            )
            for i in items
        ]

    except Exception as ex:
        logger.exception(f"Naver API fetch failed ({query}) → {ex}")
        return []
