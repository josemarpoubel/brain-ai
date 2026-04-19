"""
Helper Utilities

Common utility functions used across Brain-AI.
"""

import logging
import hashlib
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class Helpers:
    """Collection of helper utility functions."""
    
    @staticmethod
    def generate_id(prefix: str = "") -> str:
        """
        Generate a unique identifier.
        
        Args:
            prefix: Optional prefix for the ID
            
        Returns:
            Unique identifier string
        """
        timestamp = datetime.now().isoformat()
        hash_obj = hashlib.md5(timestamp.encode())
        unique_id = hash_obj.hexdigest()[:12]
        
        if prefix:
            return f"{prefix}_{unique_id}"
        return unique_id
    
    @staticmethod
    def format_timestamp(dt: datetime = None) -> str:
        """
        Format a datetime object as ISO string.
        
        Args:
            dt: Datetime object (defaults to now)
            
        Returns:
            Formatted timestamp string
        """
        if dt is None:
            dt = datetime.now()
        return dt.isoformat()
    
    @staticmethod
    def parse_json_safe(json_string: str) -> Optional[Dict[str, Any]]:
        """
        Safely parse a JSON string.
        
        Args:
            json_string: JSON string to parse
            
        Returns:
            Parsed dictionary or None if parsing fails
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            return None
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """
        Truncate text to a maximum length.
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix to add if truncated
            
        Returns:
            Truncated text string
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def calculate_hash(content: str) -> str:
        """
        Calculate SHA256 hash of content.
        
        Args:
            content: Content string to hash
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(content.encode()).hexdigest()
    
    @staticmethod
    def merge_dicts(base: Dict, override: Dict) -> Dict:
        """
        Deep merge two dictionaries.
        
        Args:
            base: Base dictionary
            override: Dictionary with values to override
            
        Returns:
            Merged dictionary
        """
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Helpers.merge_dicts(result[key], value)
            else:
                result[key] = value
        
        return result
    
    @staticmethod
    def flatten_list(nested_list: List) -> List:
        """
        Flatten a nested list.
        
        Args:
            nested_list: Potentially nested list
            
        Returns:
            Flattened list
        """
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(Helpers.flatten_list(item))
            else:
                result.append(item)
        return result
    
    @staticmethod
    def retry_async(func, max_retries: int = 3, delay: float = 1.0):
        """
        Retry an async function with exponential backoff.
        
        Args:
            func: Async function to retry
            max_retries: Maximum number of retries
            delay: Initial delay between retries
            
        Returns:
            Wrapped async function with retry logic
        """
        import asyncio
        
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    
                    if attempt < max_retries - 1:
                        wait_time = delay * (2 ** attempt)
                        await asyncio.sleep(wait_time)
            
            raise last_exception
        
        return wrapper
