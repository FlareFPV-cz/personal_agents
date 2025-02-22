from typing import Dict, Any, Optional
from enum import Enum
from datetime import datetime
import os

class ErrorSeverity(Enum):
    """Enum for error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AgentError(Exception):
    """Base exception class for agent-related errors."""
    def __init__(self, message: str, severity: ErrorSeverity = ErrorSeverity.MEDIUM, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.severity = severity
        self.details = details or {}

class ValidationError(AgentError):
    """Raised when input validation fails."""
    def __init__(self, message: str, field: str = None, **kwargs):
        super().__init__(message, severity=ErrorSeverity.MEDIUM, details={"field": field, **kwargs})

class APIError(AgentError):
    """Raised when an external API call fails."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message, severity=ErrorSeverity.HIGH, details={"status_code": status_code, "response": response})

class ConfigurationError(AgentError):
    """Raised when there's a configuration issue."""
    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(message, severity=ErrorSeverity.HIGH, details={"config_key": config_key})

class ResourceError(AgentError):
    """Raised when there's an issue with resource access or availability."""
    def __init__(self, message: str, resource_type: str, resource_id: Optional[str] = None):
        super().__init__(message, severity=ErrorSeverity.HIGH, details={"resource_type": resource_type, "resource_id": resource_id})

class AuthenticationError(AgentError):
    """Raised when there's an authentication failure."""
    def __init__(self, message: str, auth_type: str):
        super().__init__(message, severity=ErrorSeverity.CRITICAL, details={"auth_type": auth_type})

class CollaborationError(AgentError):
    """Raised when there's an error in agent collaboration."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, severity=ErrorSeverity.HIGH, details=details)

def handle_agent_error(error: Exception) -> Dict[str, Any]:
    """Formats agent errors into a standardized response format.

    Args:
        error: The exception to handle

    Returns:
        Dict[str, Any]: A formatted error response with detailed information
            including error type, message, severity, timestamp, and context
    """
    error_type = type(error).__name__
    response = {
        "success": False,
        "error": {
            "type": error_type,
            "message": str(error),
            "timestamp": datetime.now().isoformat(),
            "trace_id": os.getenv('TRACE_ID')
        }
    }
    
    if isinstance(error, AgentError):
        response["error"].update({
            "severity": error.severity.value if hasattr(error, 'severity') else None,
            "details": error.details if hasattr(error, 'details') else None
        })
    
    return response

def format_success_response(data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Formats successful responses in a standardized way.

    Args:
        data: The data to include in the response
        metadata: Optional metadata to include in the response

    Returns:
        Dict[str, Any]: A formatted success response with optional metadata
    """
    response = {
        "success": True,
        "data": data,
        "timestamp": __import__("datetime").datetime.now(__import__("datetime").UTC).isoformat()
    }
    
    if metadata:
        response["metadata"] = metadata
    
    return response