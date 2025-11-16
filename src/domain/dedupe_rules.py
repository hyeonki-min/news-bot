from typing import List
from sentence_transformers import util

from src.domain.news_entity import NewsItem
import logging
logger = logging.getLogger(__name__)


def dedupe_by_embedding(items: List[NewsItem], embed_fn, threshold: float = 0.80) -> List[NewsItem]:
    """
    임베딩 기반 중복 뉴스 제거.
    같은 클러스터의 첫 번째 뉴스를 기본 대표로 선택.
    """
    logger.info(f"Running embedding-based dedupe (threshold={threshold})")
    
    kept: List[NewsItem] = []
    kept_embeddings = []

    for news in items:
        text = (news.title or "") + " " + (news.description or "")
        vec = embed_fn(text)

        is_duplicate = False
        for k_vec in kept_embeddings:
            sim = float(util.cos_sim(vec, k_vec))
            if sim > threshold:
                logger.debug(
                    f"Duplicate detected: '{news.title[:20]}...' (similarity={sim:.3f})"
                )
                is_duplicate = True
                break

        if not is_duplicate:
            kept.append(news)
            kept_embeddings.append(vec)
    logger.info(f"Dedupe complete: {len(items)} → {len(kept)}")
    return kept
