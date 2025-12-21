import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
os.makedirs("./logs", exist_ok=True)

# Configure logging using basicConfig
logging.basicConfig(
    level=logging.WARN,
    format="%(asctime)s %(filename)s %(levelname)s %(message)s",
    handlers=[
        RotatingFileHandler(
            "./logs/api_logs.txt",
            maxBytes=1*1024*1024,  # 1MB
            backupCount=7  # Keep 7 backup files
        ),
        logging.StreamHandler()
    ]
)

# Get logger instance
_logger = logging.getLogger("citizenPortal")
_logger.setLevel(logging.INFO)


def getLogger():
    """Returns the configured logger instance for use in other modules"""
    return _logger