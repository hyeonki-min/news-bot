from collections import defaultdict
from typing import List, Dict
from src.domain.news_entity import NewsItem


def group_by_topic(items: List[NewsItem]) -> Dict[str, List[NewsItem]]:
    result = defaultdict(list)
    for item in items:
        if not item.topic or item.topic == "unknown":
            continue
        result[item.topic].append(item)
    return result


def top_n_per_topic(groups: Dict[str, List[NewsItem]], n: int = 3):
    top_items = []
    for topic, items in groups.items():
        top_items.extend(items[:n])
    return top_items
