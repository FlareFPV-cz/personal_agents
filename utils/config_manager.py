import os
import json
from typing import Any, Dict, Optional
from pathlib import Path

class ConfigManager:
    """Manages configuration settings for the framework."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.

        Args:
            config_path: Optional path to configuration file
        """
        self.config: Dict[str, Any] = {}
        self.config_path = config_path or os.getenv('AGENT_CONFIG_PATH')
        self._load_config()

    def _load_config(self):
        """Load configuration from file if available."""
        if self.config_path and os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
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