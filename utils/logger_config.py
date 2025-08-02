"""
Centralized logging configuration
"""
import logging
import sys

def setup_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    Setup and configure logger with consistent formatting
    
    Args:
        name: Logger name
        level: Logging level
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(level)
    return logger

# Create default logger
logger = setup_logger('zonal_stats')
