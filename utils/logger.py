import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Any
from datetime import datetime
from .error_handler import AgentError

class AgentLogger:
    """Configurable logging utility for agents."""

    def __init__(self, name: str, log_level: int = logging.INFO,
                 log_file: Optional[str] = None,
                 max_bytes: int = 10485760,  # 10MB
                 backup_count: int = 5,
                 format_string: Optional[str] = None,
                 propagate: bool = False):
        """Initialize logger with custom configuration.

        Args:
            name: Name of the logger instance
            log_level: Logging level (default: INFO)
            log_file: Optional file path for log output
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.logger.propagate = propagate  # Control log propagation

        # Create formatters and handlers
        format_string = format_string or '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s - {"context": %(context)s}'
        formatter = logging.Formatter(format_string)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler with rotation (if specified)
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8"
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
        # Add extra fields
        extra = {'context': {}}
        self.logger = logging.LoggerAdapter(self.logger, extra)

    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)

    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)

    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)

    def error(self, message: str, error: Optional[Exception] = None, context: Optional[Dict[str, Any]] = None, stack_info: bool = False):
        """Log error message with optional exception details and context."""
        if error:
            if isinstance(error, AgentError):
                context = context or {}
                context.update({
                    'error_type': type(error).__name__,
                    'error_details': getattr(error, 'details', {}),
                    'error_severity': getattr(error, 'severity', None)
                })
            message = f"{message} - Exception: {str(error)}"
        
        self.logger.error(message, extra={'context': context or {}}, stack_info=stack_info)

    def set_context(self, **kwargs):
        """Set context for all subsequent log messages."""
        self.logger.extra['context'].update(kwargs)

    def clear_context(self):
        """Clear all context data."""
        self.logger.extra['context'] = {}

    def get_context(self) -> Dict[str, Any]:
        """Get current logging context."""
        return self.logger.extra['context'].copy()

    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)

    def exception(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log exception message with traceback."""
        self.logger.exception(message, extra={'context': context or {}})