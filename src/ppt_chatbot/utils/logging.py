from loguru import logger
import sys

def configure_logging():
    """Configure structured logging with rotation"""
    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    logger.add(
        "logs/ppt_chatbot.log",
        rotation="1 week",
        retention="1 month",
        level="DEBUG"
    )
    return logger