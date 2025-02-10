class AgentError(Exception):
    """Base exception class for agent-related errors."""
    pass

class ValidationError(AgentError):
    """Raised when input validation fails."""
    pass

class APIError(AgentError):
    """Raised when an external API call fails."""
    pass

class ConfigurationError(AgentError):
    """Raised when there's a configuration issue."""
    pass

def handle_agent_error(error: Exception) -> dict:
    """Formats agent errors into a standardized response format.

    Args:
        error: The exception to handle

    Returns:
        dict: A formatted error response
    """
    error_type = type(error).__name__
    return {
        "success": False,
        "error": {
            "type": error_type,
            "message": str(error)
        }
    }

def format_success_response(data: dict) -> dict:
    """Formats successful responses in a standardized way.

    Args:
        data: The data to include in the response

    Returns:
        dict: A formatted success response
    """
    return {
        "success": True,
        "data": data
    }