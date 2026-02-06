import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

logger = logging.getLogger()


def transform_date(date_str):
    dt = datetime.strptime(date_str, "%A, %B %d, %Y %I:%M %p")
    return dt.strftime("%Y-%m-%d %H:%M:%S.000Z")
