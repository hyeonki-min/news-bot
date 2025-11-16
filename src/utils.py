from datetime import datetime, timedelta


def parse_rfc822(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %z")


def yesterday_md() -> str:
    return (datetime.now() - timedelta(days=1)).strftime("%m%d%y")


def clean_html(text: str) -> str:
    return (
        text.replace("<b>", "")
        .replace("</b>", "")
        .replace("&quot;", '"')
        .replace("&amp;", "&")
    )