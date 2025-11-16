import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()  # .env 로드


@dataclass
class Config:
    naver_client_id: str
    naver_client_secret: str
    slack_webhook_url: str
    csv_file_path: str


def load_config() -> Config:
    return Config(
        naver_client_id=os.getenv("NAVER_CLIENT_ID"),
        naver_client_secret=os.getenv("NAVER_CLIENT_SECRET"),
        slack_webhook_url=os.getenv("SLACK_WEBHOOK_URL"),
        csv_file_path=os.getenv("CSV_FILE_PATH", "keywords.csv"),
    )
