import logging
from pythonjsonlogger import jsonlogger
import sys


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d"
    )
    log_handler.setFormatter(formatter)

    # Clear existing handlers to avoid duplication
    logger.handlers = []
    logger.addHandler(log_handler)
