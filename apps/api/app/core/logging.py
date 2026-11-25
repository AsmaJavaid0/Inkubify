import logging
import sys


def setup_logging(app_env: str = "development") -> None:
    """Configure application logging without leaking PII or stack traces."""
    level = logging.DEBUG if app_env == "development" else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        stream=sys.stdout,
    )
    # Suppress overly verbose third-party HTTP debug logs that could include headers/tokens
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
