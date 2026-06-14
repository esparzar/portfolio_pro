import logging
from logging.config import dictConfig

from flask import Flask


def configure_logging(app: Flask) -> None:
    """Configure application logging for local and production use."""
    level = "DEBUG" if app.config.get("DEBUG") else "INFO"
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {"level": level, "handlers": ["console"]},
        }
    )
    app.logger.setLevel(getattr(logging, level))
