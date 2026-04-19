"""
Brain-AI Configuration

System configuration management.
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    "system": {
        "name": "Brain-AI",
        "version": "0.1.0",
        "debug": False,
        "log_level": "INFO"
    },
    "orchestrator": {
        "max_concurrent_tasks": 5,
        "task_timeout": 300,
        "retry_attempts": 3
    },
    "agents": {
        "planner": {
            "enabled": True,
            "model": "default"
        },
        "coder": {
            "enabled": True,
            "language": "python",
            "style_guide": "PEP8"
        },
        "reviewer": {
            "enabled": True,
            "checks": ["syntax", "style", "security"]
        },
        "memory": {
            "enabled": True,
            "obsidian_path": "memory/obsidian",
            "sqlite_path": "memory/sqlite/brain.db",
            "cache_path": "memory/cache"
        },
        "tester": {
            "enabled": True,
            "test_framework": "pytest",
            "coverage_enabled": True
        }
    },
    "llm": {
        "default_provider": "openrouter",
        "models": {
            "default": "openai/gpt-4",
            "local": "llama2"
        },
        "parameters": {
            "temperature": 0.7,
            "max_tokens": 2048,
            "timeout": 30
        }
    },
    "memory": {
        "semantic": {
            "enabled": True,
            "path": "memory/obsidian"
        },
        "structured": {
            "enabled": True,
            "path": "memory/sqlite/brain.db",
            "fts_enabled": True
        },
        "cache": {
            "enabled": True,
            "path": "memory/cache",
            "compression": "cbor",
            "ttl_seconds": 3600
        }
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "logs/brain_ai.log",
        "console": True
    }
}


class Config:
    """
    Configuration manager for Brain-AI system.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config_path = config_path
        self.config = DEFAULT_CONFIG.copy()
        
        if config_path:
            self.load_from_file(config_path)
        
        # Override with environment variables
        self._load_from_env()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., "llm.default_provider")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., "llm.default_provider")
            value: Value to set
        """
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def load_from_file(self, path: str) -> bool:
        """
        Load configuration from a JSON file.
        
        Args:
            path: Path to configuration file
            
        Returns:
            True if loading was successful
        """
        try:
            config_file = Path(path)
            if config_file.exists():
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                
                # Deep merge with defaults
                self._deep_merge(file_config)
                return True
        except Exception as e:
            print(f"Error loading config file: {e}")
        
        return False
    
    def save_to_file(self, path: str) -> bool:
        """
        Save current configuration to a JSON file.
        
        Args:
            path: Path to save configuration
            
        Returns:
            True if saving was successful
        """
        try:
            config_file = Path(path)
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving config file: {e}")
            return False
    
    def _deep_merge(self, override: Dict) -> None:
        """
        Deep merge override configuration into current config.
        
        Args:
            override: Dictionary to merge
        """
        for key, value in override.items():
            if key in self.config and isinstance(self.config[key], dict) and isinstance(value, dict):
                self._deep_merge_recursive(self.config[key], value)
            else:
                self.config[key] = value
    
    def _deep_merge_recursive(self, base: Dict, override: Dict) -> None:
        """Recursively merge dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge_recursive(base[key], value)
            else:
                base[key] = value
    
    def _load_from_env(self) -> None:
        """Load configuration overrides from environment variables."""
        # System settings
        if os.getenv("BRAIN_AI_DEBUG"):
            self.set("system.debug", os.getenv("BRAIN_AI_DEBUG").lower() == "true")
        
        if os.getenv("BRAIN_AI_LOG_LEVEL"):
            self.set("logging.level", os.getenv("BRAIN_AI_LOG_LEVEL"))
        
        # LLM settings
        if os.getenv("OPENROUTER_API_KEY"):
            self.set("llm.api_key", os.getenv("OPENROUTER_API_KEY"))
        
        if os.getenv("BRAIN_AI_DEFAULT_MODEL"):
            self.set("llm.models.default", os.getenv("BRAIN_AI_DEFAULT_MODEL"))
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get configuration as dictionary.
        
        Returns:
            Complete configuration dictionary
        """
        return self.config.copy()
    
    def __repr__(self) -> str:
        return f"Config({json.dumps(self.config, indent=2)})"


# Global configuration instance
_global_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config


def init_config(config_path: Optional[str] = None) -> Config:
    """Initialize the global configuration."""
    global _global_config
    _global_config = Config(config_path)
    return _global_config
