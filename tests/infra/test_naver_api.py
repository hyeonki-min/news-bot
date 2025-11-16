from unittest.mock import patch
from src.infra.naver_api import fetch_news


@patch("src.infra.naver_api.requests.get")
def test_fetch_news_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "items": [
            {
                "title": "<b>경제</b> 뉴스",
                "description": "테스트",
                "link": "http://example.com",
                "originallink": "http://origin.com",
                "pubDate": "Mon, 01 Jan 2024 10:00:00 +0900",
            }
        ]
    }

    result = fetch_news("경제", "id", "secret")
    assert len(result) == 1
    assert result[0].title == "경제 뉴스"
