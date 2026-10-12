"""
Logging configuration for GraphRAG Knowledge System.
Gracefully uses loguru if available, otherwise falls back to standard Python logging.
"""
import sys

try:
    from loguru import logger

    def setup_logger():
        logger.remove()
        logger.add(
            sys.stdout,
            level="INFO",
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            colorize=True,
        )
        return logger

    app_logger = setup_logger()

except ImportError:
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    app_logger = logging.getLogger("graphrag")

    def setup_logger():
        return app_logger
