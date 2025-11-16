from src.core.db import SessionLocal, Base, engine
from src.core.config import load_config
from src.services.publish import publish_topic_top3
from src.infra.embedding_client import EmbeddingClient
from src.domain.dedupe_rules import dedupe_by_embedding

from src.infra.naver_api import fetch_news
from src.core.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)
client = EmbeddingClient()


def main():
    logger.info("Starting news collection batch...")

    cfg = load_config()
    db = SessionLocal()

    # 키워드 로딩
    with open(cfg.csv_file_path, "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f]
    logger.debug(f"Loaded keywords: {keywords}")

    # 뉴스 수집
    collected = []
    for kw in keywords:
        collected.extend(fetch_news(kw, cfg.naver_client_id, cfg.naver_client_secret))
    logger.debug(f"Fetched {len(collected)}")
    # 중복 제거
    deduped = dedupe_by_embedding(collected, client.embed, threshold=0.80)
    logger.debug(f"Total raw news count {len(deduped)}")
    # 4) Slack 성공한 것만 DB 일괄 저장
    publish_topic_top3(db, deduped, cfg.slack_webhook_url)


if __name__ == "__main__":
    main()
