"""
Simple A2A Server Implementation for Agentic GraphRAG System

This module implements a simple A2A server following the Google ADK examples
that wraps the KG Agent with MCP integration for local operation.
"""

import asyncio
import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime
import uvicorn

from google.adk.a2a.utils.agent_to_a2a import to_a2a

from config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.google_cloud.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgenticGraphRAGServer:
    """
    Simple A2A server for the Agentic GraphRAG system using Google ADK.
    
    Provides A2A protocol endpoints by wrapping the KG Agent.
    """
    
    def __init__(self):
        self.a2a_app = None
        self.kg_agent = None
        self.start_time = datetime.now()
        
    async def initialize(self):
        """Initialize A2A server using Google ADK agent wrapper"""
        logger.info("Initializing Agentic GraphRAG A2A Server")
        
        # Initialize Google Cloud if configured (local mode - skipped)
        if config.google_cloud.project_id:
            logger.info("Google Cloud initialization skipped (running in local mode)")
        
        # Import and create KG Agent
        from agents.kg_agent import KnowledgeGraphAgent
        self.kg_agent = KnowledgeGraphAgent()
        await self.kg_agent.initialize()
        
        # Create A2A app using Google ADK utility
        # This wraps our KG Agent as an A2A compatible server
        self.a2a_app = to_a2a(
            self.kg_agent.agent,  # The underlying Google ADK agent
            port=config.a2a.port
        )
        
        logger.info(f"A2A server initialized on port {config.a2a.port}")
    
    async def start(self):
        """Start the A2A server with Uvicorn"""
        if not self.a2a_app:
            await self.initialize()
        
        logger.info("🚀 Starting Agentic GraphRAG A2A Server with Uvicorn...")
        logger.info(f"   Server: http://localhost:{config.a2a.port}")
        logger.info(f"   MCP Server: {config.mcp.server_url}")
        logger.info("   Agent: KnowledgeGraph with MCP tools")
        
        # Start Uvicorn server with the A2A app
        config_uvicorn = uvicorn.Config(
            app=self.a2a_app,
            host="0.0.0.0",
            port=config.a2a.port,
            log_level="info"
        )
        server = uvicorn.Server(config_uvicorn)
        
        # This will block and keep the server running
        await server.serve()
    
    async def shutdown(self):
        """Shutdown the A2A server"""
        if self.kg_agent:
            await self.kg_agent.cleanup()
        logger.info("A2A server shutdown completed")
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "status": "running" if self.a2a_app else "stopped",
            "port": config.a2a.port,
            "start_time": self.start_time.isoformat(),
            "agent_type": "KnowledgeGraph with MCP"
        }
    
    def set_kg_agent(self, kg_agent):
        """Set the KG agent (compatibility method)"""
        self.kg_agent = kg_agent

# Global instance for external Uvicorn access
_server_instance = None

async def get_a2a_app():
    """Get the A2A app for external Uvicorn usage"""
    global _server_instance
    if not _server_instance:
        _server_instance = AgenticGraphRAGServer()
        await _server_instance.initialize()
    return _server_instance.a2a_app

# For external uvicorn command: uvicorn server.a2a_server:app
app = None

async def init_app():
    """Initialize app for external access"""
    global app
    if not app:
        app = await get_a2a_app()
    return app