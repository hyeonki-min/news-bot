from src.infra.slack_api import send_slack_message
from src.services.topic_service import detect_topic
from src.domain.topic_rules import group_by_topic, top_n_per_topic
from src.repositories.news_repository import save_news_bulk
from src.models.news_model import NewsItemModel


def publish_topic_top3(db, items, slack_url):
    # 1) 토픽 분류
    for item in items:
        item.topic = detect_topic(item)

    # 2) 토픽별로 묶기
    by_topic = group_by_topic(items)

    # 3) 각 토픽 상위 3개만 추출
    top_items = top_n_per_topic(by_topic, n=3)

    # 4) Slack 전송
    sent_items = []
    for news in top_items:
        ok = send_slack_message(news, slack_url)
        if ok:
            sent_items.append(news)

    # 5) Slack 전송 성공한 것만 DB 저장
    save_news_bulk(db, sent_items)

    return sent_items