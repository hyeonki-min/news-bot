from src.infra.embedding_client import EmbeddingClient
from src.domain.topic_classifier import classify_topic

client = EmbeddingClient()


def detect_topic(news):
    # news: NewsItem (domain entity)
    return classify_topic(news.description, client.embed, client.anchor_embeddings)
