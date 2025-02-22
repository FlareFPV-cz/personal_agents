import os
import json
from typing import Any, Dict, Optional, Union
from pathlib import Path
from dotenv import load_dotenv
from .error_handler import ConfigurationError, ErrorSeverity

class ConfigManager:
    """Manages configuration settings for the framework."""

    def __init__(self, config_path: Optional[str] = None, env_file: str = ".env"):
        """Initialize configuration manager.

        Args:
            config_path: Optional path to configuration file
            env_file: Path to .env file (default: ".env")

        Raises:
            ConfigurationError: If required environment variables are missing
        """
        self.config: Dict[str, Any] = {}
        self.config_path = config_path or os.getenv('AGENT_CONFIG_PATH')
        self.env_file = env_file
        
        self._load_env()
        self._load_config()
        self._validate_required_env()

    def _load_env(self):
        """Load environment variables from .env file."""
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
        else:
            raise ConfigurationError(f"Environment file not found: {self.env_file}")

    def _validate_required_env(self):
        """Validate required environment variables."""
        required_vars = ['GROQ_API_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ConfigurationError(
                f"Missing required environment variables: {', '.join(missing_vars)}",
                severity=ErrorSeverity.CRITICAL
            )

    def _load_config(self):
        """Load configuration from file if available.
        
        Raises:
            ConfigurationError: If config file exists but cannot be loaded
        """
        if not self.config_path:
            return
            
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in config file: {e}", config_key=self.config_path)
        except Exception as e:
            raise ConfigurationError(f"Error loading config file: {e}", config_key=self.config_path)

    def get(self, key: str, default: Any = None, required: bool = False) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found
            required: If True, raise error when key not found

        Returns:
            Configuration value

        Raises:
            ConfigurationError: If key is required but not found
        """
        value = self.config.get(key, default)
        
        if required and value is None:
            raise ConfigurationError(f"Required configuration key not found: {key}", config_key=key)
            
        return value

    def set(self, key: str, value: Any, save: bool = True):
        """Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
            save: If True, save config to file after setting

        Raises:
            ConfigurationError: If value cannot be JSON serialized
        """
        try:
            # Verify value is JSON serializable
            json.dumps({key: value})
            self.config[key] = value
            
            if save:
                self.save()
        except TypeError as e:
            raise ConfigurationError(f"Value not JSON serializable: {e}", config_key=key)
        self.config[key] = value

    def save(self):
        """Save current configuration to file."""
        if self.config_path:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)

    def load_env_vars(self, prefix: str = 'AGENT_'):
        """Load environment variables with specified prefix into config.

        Args:
            prefix: Prefix for environment variables to load
        """
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                self.config[config_key] = value

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values.

        Returns:
            Dictionary of all configuration values
        """
        return self.config.copy()