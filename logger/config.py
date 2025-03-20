import sys
from loguru import logger
from settings import ENVIRONMENT, LOG_LEVEL, LOG_FILE_PATH

# Remove default loguru handler
logger.remove()

if ENVIRONMENT == "development":
    logger.add(
        sys.stderr,
        level=LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
    )
else:
    logger.add(
        LOG_FILE_PATH,
        level=LOG_LEVEL,
        rotation="10 MB",  # Create a new log file after 10MB
        retention="7 days",  # Keep logs for 7 days
        compression="zip",  # Compress old logs
        format="{time} | {level} | {message}",
    )
