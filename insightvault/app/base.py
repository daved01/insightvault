import logging
from datetime import datetime

class BaseApp:
    def __init__(self, name: str = "insightvault") -> None:
        self.name = name
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup application logger with console handler"""
        # Create logger
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        
        # Avoid adding handlers multiple times
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter('%(asctime)s [%(name)s] | %(message)s', 
                                datefmt='%Y-%m-%d %H:%M:%S')
            )
            logger.addHandler(console_handler)
        
        return logger
