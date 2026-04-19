"""
Validators

Input validation utilities for Brain-AI.
"""

import re
import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class Validators:
    """Collection of validation utility functions."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate an email address.
        
        Args:
            email: Email string to validate
            
        Returns:
            True if valid email format
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate a URL.
        
        Args:
            url: URL string to validate
            
        Returns:
            True if valid URL format
        """
        pattern = r'^https?://[^\s]+$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def validate_json_structure(data: Any, schema: Dict[str, type]) -> Tuple[bool, List[str]]:
        """
        Validate that a dictionary matches expected schema.
        
        Args:
            data: Dictionary to validate
            schema: Expected schema with field names and types
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        if not isinstance(data, dict):
            return False, ["Data must be a dictionary"]
        
        for field, expected_type in schema.items():
            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(data[field], expected_type):
                errors.append(f"Field '{field}' must be of type {expected_type.__name__}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_code_language(code: str, language: str = "python") -> bool:
        """
        Basic validation of code syntax by language.
        
        Args:
            code: Code string to validate
            language: Programming language
            
        Returns:
            True if code appears valid
        """
        if language.lower() == "python":
            try:
                compile(code, '<string>', 'exec')
                return True
            except SyntaxError:
                return False
        
        # Add support for other languages as needed
        return True
    
    @staticmethod
    def validate_non_empty(value: Any, field_name: str = "value") -> Tuple[bool, str]:
        """
        Validate that a value is not empty.
        
        Args:
            value: Value to check
            field_name: Name of the field for error messages
            
        Returns:
            Tuple of (is_valid, error message or empty string)
        """
        if value is None:
            return False, f"{field_name} cannot be None"
        
        if isinstance(value, str) and not value.strip():
            return False, f"{field_name} cannot be empty"
        
        if isinstance(value, (list, dict)) and len(value) == 0:
            return False, f"{field_name} cannot be empty"
        
        return True, ""
    
    @staticmethod
    def validate_range(value: int or float, min_val: int or float, 
                       max_val: int or float, field_name: str = "value") -> Tuple[bool, str]:
        """
        Validate that a numeric value is within range.
        
        Args:
            value: Numeric value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            field_name: Name of the field for error messages
            
        Returns:
            Tuple of (is_valid, error message or empty string)
        """
        if value < min_val:
            return False, f"{field_name} must be at least {min_val}"
        
        if value > max_val:
            return False, f"{field_name} must be at most {max_val}"
        
        return True, ""
    
    @staticmethod
    def validate_list_items(items: List, item_type: type, 
                           field_name: str = "items") -> Tuple[bool, List[str]]:
        """
        Validate that all items in a list are of expected type.
        
        Args:
            items: List to validate
            item_type: Expected type for all items
            field_name: Name of the field for error messages
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        if not isinstance(items, list):
            return False, [f"{field_name} must be a list"]
        
        for i, item in enumerate(items):
            if not isinstance(item, item_type):
                errors.append(f"{field_name}[{i}] must be of type {item_type.__name__}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Basic validation of API key format.
        
        Args:
            api_key: API key string to validate
            
        Returns:
            True if API key appears valid
        """
        if not api_key or len(api_key) < 10:
            return False
        
        # Check for common API key patterns
        if re.match(r'^[a-zA-Z0-9_-]+$', api_key):
            return True
        
        return False
