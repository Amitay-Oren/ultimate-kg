"""
A2A Server Configuration for Google ADK Agents

This module provides configuration and setup for an A2A server
hosting Google ADK agents with proper Google Cloud integration.
"""

import os
import asyncio
import logging
from typing import Dict, List, Optional
from pathlib import Path

from a2a_sdk import A2AServer, A2AServerConfig
from google.cloud import aiplatform
from google.auth import default
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GoogleCloudA2AServerConfig:
    """Configuration class for A2A server with Google Cloud integration"""
    
    def __init__(self):
        self.server_host = os.getenv("A2A_SERVER_HOST", "0.0.0.0")
        self.server_port = int(os.getenv("A2A_SERVER_PORT", "8080"))
        self.network_mode = os.getenv("A2A_NETWORK_MODE", "development")
        
        # Google Cloud configuration
        self.google_project = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.vertex_ai_location = os.getenv("VERTEX_AI_LOCATION", "us-central1")
        self.google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        # A2A protocol configuration
        self.a2a_protocol_version = os.getenv("A2A_PROTOCOL_VERSION", "1.0")
        self.max_concurrent_requests = int(os.getenv("A2A_MAX_CONCURRENT_REQUESTS", "100"))
        self.request_timeout = int(os.getenv("A2A_REQUEST_TIMEOUT", "30"))
        
        # Security configuration
        self.tls_enabled = os.getenv("A2A_TLS_ENABLED", "false").lower() == "true"
        self.tls_cert_file = os.getenv("A2A_TLS_CERT_FILE")
        self.tls_key_file = os.getenv("A2A_TLS_KEY_FILE")
        self.api_key_secret = os.getenv("A2A_AGENT_API_KEY_SECRET")
        
        # Monitoring configuration
        self.enable_metrics = os.getenv("A2A_ENABLE_METRICS", "true").lower() == "true"
        self.metrics_port = int(os.getenv("A2A_METRICS_PORT", "9090"))
        
    def validate(self) -> bool:
        """Validate configuration settings"""
        if not self.google_project:
            logger.error("GOOGLE_CLOUD_PROJECT environment variable is required")
            return False
            
        if self.tls_enabled and (not self.tls_cert_file or not self.tls_key_file):
            logger.error("TLS certificate and key files required when TLS is enabled")
            return False
            
        return True

class A2AServerManager:
    """Manager class for A2A server with Google Cloud integration"""
    
    def __init__(self, config: GoogleCloudA2AServerConfig):
        self.config = config
        self.server: Optional[A2AServer] = None
        self.registered_agents: Dict[str, any] = {}
        
    async def initialize_google_cloud(self):
        """Initialize Google Cloud services"""
        try:
            # Initialize Vertex AI
            aiplatform.init(
                project=self.config.google_project,
                location=self.config.vertex_ai_location
            )
            
            # Verify authentication
            credentials, project = default()
            logger.info(f"Google Cloud initialized for project: {project}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Cloud: {e}")
            raise
    
    async def create_server(self) -> A2AServer:
        """Create and configure A2A server"""
        server_config = A2AServerConfig(
            host=self.config.server_host,
            port=self.config.server_port,
            protocol_version=self.config.a2a_protocol_version,
            max_concurrent_requests=self.config.max_concurrent_requests,
            request_timeout=self.config.request_timeout,
            enable_tls=self.config.tls_enabled,
            tls_cert_file=self.config.tls_cert_file,
            tls_key_file=self.config.tls_key_file,
            enable_metrics=self.config.enable_metrics,
            metrics_port=self.config.metrics_port
        )
        
        self.server = A2AServer(server_config)
        return self.server
    
    async def register_agent(self, agent, capabilities: Dict):
        """Register an agent with the A2A server"""
        if not self.server:
            raise RuntimeError("Server not initialized")
            
        agent_id = agent.name
        self.registered_agents[agent_id] = {
            "agent": agent,
            "capabilities": capabilities,
            "registered_at": asyncio.get_event_loop().time()
        }
        
        await self.server.register_agent(agent_id, capabilities)
        logger.info(f"Registered agent: {agent_id}")
    
    async def start_server(self):
        """Start the A2A server"""
        if not self.server:
            raise RuntimeError("Server not created")
            
        logger.info(f"Starting A2A server on {self.config.server_host}:{self.config.server_port}")
        
        if self.config.network_mode == "production":
            logger.info("Running in production mode with enhanced security")
        
        await self.server.start()
    
    async def shutdown(self):
        """Gracefully shutdown the server"""
        if self.server:
            logger.info("Shutting down A2A server")
            await self.server.shutdown()
    
    def get_server_info(self) -> Dict:
        """Get server information and status"""
        return {
            "server_host": self.config.server_host,
            "server_port": self.config.server_port,
            "network_mode": self.config.network_mode,
            "protocol_version": self.config.a2a_protocol_version,
            "registered_agents": len(self.registered_agents),
            "agent_list": list(self.registered_agents.keys()),
            "google_project": self.config.google_project,
            "vertex_ai_location": self.config.vertex_ai_location
        }

async def setup_a2a_server_with_google_adk():
    """
    Complete setup function for A2A server with Google ADK agents
    """
    # Load configuration
    config = GoogleCloudA2AServerConfig()
    
    if not config.validate():
        raise RuntimeError("Invalid configuration")
    
    # Create server manager
    server_manager = A2AServerManager(config)
    
    # Initialize Google Cloud
    await server_manager.initialize_google_cloud()
    
    # Create A2A server
    await server_manager.create_server()
    
    logger.info("A2A server setup completed successfully")
    logger.info(f"Server info: {server_manager.get_server_info()}")
    
    return server_manager

def create_production_server_config():
    """Create production server configuration"""
    return {
        "host": "0.0.0.0",
        "port": 8080,
        "workers": 4,
        "log_level": "info",
        "access_log": True,
        "use_colors": False,
        "server_header": False,
        "date_header": False
    }

async def main():
    """Main function for running A2A server"""
    try:
        # Setup server
        server_manager = await setup_a2a_server_with_google_adk()
        
        # Start server
        await server_manager.start_server()
        
    except Exception as e:
        logger.error(f"Failed to start A2A server: {e}")
        raise
    finally:
        if 'server_manager' in locals():
            await server_manager.shutdown()

def run_production_server():
    """Run server in production mode with uvicorn"""
    config = create_production_server_config()
    
    uvicorn.run(
        "a2a_server_config:main",
        **config
    )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="A2A Server for Google ADK Agents")
    parser.add_argument("--mode", choices=["development", "production"], 
                       default="development", help="Server mode")
    parser.add_argument("--validate", action="store_true", 
                       help="Validate configuration only")
    parser.add_argument("--port", type=int, help="Server port")
    
    args = parser.parse_args()
    
    if args.port:
        os.environ["A2A_SERVER_PORT"] = str(args.port)
    
    os.environ["A2A_NETWORK_MODE"] = args.mode
    
    if args.validate:
        config = GoogleCloudA2AServerConfig()
        if config.validate():
            print("Configuration is valid")
        else:
            print("Configuration validation failed")
            exit(1)
    else:
        if args.mode == "production":
            run_production_server()
        else:
            asyncio.run(main())