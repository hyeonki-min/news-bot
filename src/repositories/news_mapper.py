from src.domain.news_entity import NewsItem
from src.models.news_model import NewsItemModel

class NewsMapper:

    @staticmethod
    def to_model(entity: NewsItem) -> NewsItemModel:
        return NewsItemModel(
            title=entity.title,
            description=entity.description,
            link=entity.link,
            original_link=entity.original_link,
            pub_date=entity.pub_date,
        )

    @staticmethod
    def to_entity(model: NewsItemModel) -> NewsItem:
        return NewsItem(
            title=model.title,
            description=model.description,
            link=model.link,
            original_link=model.original_link,
            pub_date=model.pub_date,
        )
