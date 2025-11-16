from typing import Dict
from sentence_transformers import util
from src.domain.topic_anchors import TOPIC_ANCHORS

def classify_topic(text: str, embed_func, ANCHOR_EMBEDDINGS) -> str:
    """
    text: 뉴스 본문 or 제목
    embed_func: embedding_client.embed
    ANCHOR_EMBEDDINGS: embedding_client.anchor_embeddings
    """
    text_vec = embed_func(text)

    scores: Dict[str, float] = {}

    for topic, anchor_vecs in ANCHOR_EMBEDDINGS.items():
        # 여러 anchor 중 가장 높은 similarity 사용
        sim_values = [util.cos_sim(text_vec, a_vec).item() for a_vec in anchor_vecs]
        max_sim = max(sim_values)
        scores[topic] = max_sim
    best_topic = max(scores, key=scores.get)
    best_score = scores[best_topic]
    if best_score < 0.45:
        return "unknown"

    return best_topic
