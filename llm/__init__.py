"""
Brain-AI LLM Layer

Model abstraction layer supporting multiple providers:
- Cloud LLMs (OpenAI, OpenRouter)
- Local Models (Ollama, Llama.cpp)
"""

from .llm_interface import LLMInterface
from .openrouter_client import OpenRouterClient
from .local_client import LocalClient

__all__ = [
    'LLMInterface',
    'OpenRouterClient',
    'LocalClient'
]
