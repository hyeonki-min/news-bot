import json
import requests
from datetime import datetime

from src.domain.news_entity import NewsItem
import logging
logger = logging.getLogger(__name__)


def send_slack_message(news: NewsItem, webhook_url: str) -> bool:
    try:
        resp = requests.post(
            webhook_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(news.to_slack_payload()),
        )
        resp.raise_for_status()
        return True

    except Exception as ex:
        logger.exception(f"Slack error: {e}")
        return False
