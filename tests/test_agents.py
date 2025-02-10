import unittest
from utils.error_handler import handle_agent_error, format_success_response
from core.base_agent import BaseAgent

class TestErrorHandler(unittest.TestCase):
    """Test cases for error handling utilities."""

    def test_error_handling(self):
        """Test error handling formatting."""
        test_error = ValueError("Test error message")
        result = handle_agent_error(test_error)
        
        self.assertFalse(result["success"])
        self.assertEqual(result["error"]["type"], "ValueError")
        self.assertEqual(result["error"]["message"], "Test error message")

    def test_success_response(self):
        """Test success response formatting."""
        test_data = {"key": "value"}
        result = format_success_response(test_data)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["data"], test_data)

if __name__ == "__main__":
    unittest.main()