"""
Agentic GraphRAG System with A2A Protocol Integration

A comprehensive multi-agent system that integrates Google ADK agents 
with Cognee GraphRAG via A2A Protocol endpoints for knowledge ingestion, 
fact extraction, and connection discovery.
"""

__version__ = "0.1.0"
__author__ = "Ultimate KG Project"

from .config import config
from .server.a2a_server import AgenticGraphRAGServer
from .agents.kg_agent import KnowledgeGraphAgent
from .agents.notification_manager import NotificationManager

__all__ = [
    "config",
    "AgenticGraphRAGServer", 
    "KnowledgeGraphAgent",
    "NotificationManager"
]