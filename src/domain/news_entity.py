from dataclasses import dataclass
from datetime import datetime

@dataclass
class NewsItem:
    title: str
    description: str
    link: str
    original_link: str
    pub_date: datetime
    topic: str = None

    def to_slack_payload(self):
        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📰 [{self.topic}] {self.title}"
                    }
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": self.description}
                },
                {
                    "type": "context",
                    "elements": [
                        {"type": "mrkdwn", "text": f"<{self.original_link}|{self.link}>"}
                    ]
                }
            ]
        }

