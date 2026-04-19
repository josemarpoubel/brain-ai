"""
LLM Interface

Abstract base interface for LLM providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, AsyncIterator
import logging

logger = logging.getLogger(__name__)


class LLMInterface(ABC):
    """
    Abstract base interface for all LLM providers.
    
    This interface ensures model-agnostic reasoning execution
    across different LLM backends.
    """
    
    def __init__(self, model_name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the LLM interface.
        
        Args:
            model_name: Name/identifier of the model to use
            config: Optional configuration dictionary
        """
        self.model_name = model_name
        self.config = config or {}
        logger.info(f"LLM Interface initialized with model: {model_name}")
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: Input prompt string
            **kwargs: Additional generation parameters
            
        Returns:
            Generated response string
        """
        pass
    
    @abstractmethod
    async def generate_stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """
        Generate a streaming response from the LLM.
        
        Args:
            prompt: Input prompt string
            **kwargs: Additional generation parameters
            
        Yields:
            Chunks of generated text
        """
        pass
    
    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Execute a chat completion with conversation history.
        
        Args:
            messages: List of message dictionaries with role and content
            **kwargs: Additional completion parameters
            
        Returns:
            Generated response string
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model.
        
        Returns:
            Dictionary containing model information
        """
        pass
    
    def validate_response(self, response: str) -> bool:
        """
        Validate that a response meets basic quality criteria.
        
        Args:
            response: Response string to validate
            
        Returns:
            True if response is valid
        """
        if not response or not response.strip():
            return False
        return True
    
    def format_prompt(self, template: str, **variables) -> str:
        """
        Format a prompt template with variables.
        
        Args:
            template: Prompt template string
            **variables: Variables to substitute in template
            
        Returns:
            Formatted prompt string
        """
        try:
            return template.format(**variables)
        except KeyError as e:
            logger.error(f"Missing variable in prompt template: {e}")
            return template
