from unittest.mock import patch
from src.infra.slack_api import send_slack_message
from src.domain.news_entity import NewsItem
from datetime import datetime


@patch("src.infra.slack_api.requests.post")
def test_send_slack_message(mock_post):
    mock_post.return_value.status_code = 200

    news = NewsItem(
        title="테스트",
        description="테스트 내용",
        link="http://a",
        original_link="http://b",
        pub_date=datetime.now(),
    )

    result = send_slack_message(news, "http://dummy")
    assert result is True
