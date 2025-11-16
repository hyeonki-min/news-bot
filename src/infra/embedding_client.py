from sentence_transformers import SentenceTransformer
from functools import lru_cache
from src.domain.topic_anchors import TOPIC_ANCHORS


class EmbeddingClient:

    def __init__(self, model_name="jhgan/ko-sroberta-multitask"):
        self.model = SentenceTransformer(model_name)

        self.anchor_embeddings = {
            topic: [self.model.encode(a, normalize_embeddings=True) for a in anchors]
            for topic, anchors in TOPIC_ANCHORS.items()
        }
        
    @lru_cache(maxsize=2048)
    def embed(self, text: str):
        return self.model.encode(text)
