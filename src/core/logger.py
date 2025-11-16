import logging
import logging.handlers
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def setup_logging():
    """
    앱 공통 로깅 설정.
    - 콘솔: INFO 이상
    - 파일: DEBUG 이상
    - rotating file handler (최대 10MB, 백업 5개)
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] (%(name)s): %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 콘솔 핸들러
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    # 파일 핸들러 (rotate)
    fh = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # 기존 핸들러 제거 후 추가
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(ch)
    logger.addHandler(fh)
