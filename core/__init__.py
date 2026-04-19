"""
Brain-AI Core Orchestration Engine

This module contains the central orchestration system responsible for:
- Interpreting user requests
- Decomposing tasks into subtasks
- Routing tasks to specialized agents
- Managing execution flow and state
"""

from .orchestrator import Orchestrator

__all__ = ['Orchestrator']
