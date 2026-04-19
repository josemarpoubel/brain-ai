"""
Base Agent Module

Abstract base class for all Brain-AI agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all cognitive agents in Brain-AI.
    
    All specialized agents must inherit from this class and implement
    the execute method.
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a base agent.
        
        Args:
            name: Unique identifier for this agent
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        logger.info(f"Agent '{name}' initialized")
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task assigned to this agent.
        
        Args:
            task: Task dictionary containing task details
            
        Returns:
            Dictionary containing execution results
        """
        pass
    
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """
        Validate if a task is suitable for this agent.
        
        Args:
            task: Task dictionary to validate
            
        Returns:
            True if task is valid, False otherwise
        """
        return "type" in task
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status.
        
        Returns:
            Dictionary containing status information
        """
        return {
            "name": self.name,
            "active": True,
            "config": self.config
        }
