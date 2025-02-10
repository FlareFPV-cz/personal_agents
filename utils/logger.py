import logging
import os
from typing import Optional

class AgentLogger:
    """Configurable logging utility for agents."""

    def __init__(self, name: str, log_level: int = logging.INFO,
                 log_file: Optional[str] = None):
        """Initialize logger with custom configuration.

        Args:
            name: Name of the logger instance
            log_level: Logging level (default: INFO)
            log_file: Optional file path for log output
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Create formatters and handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler (if specified)
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)

    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)

    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)

    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)

    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)

    def exception(self, message: str):
        """Log exception message with traceback."""
        self.logger.exception(message)