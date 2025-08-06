"""
Configuration module for Agentic GraphRAG A2A System.

This module provides centralized configuration management for the system,
integrating A2A, Google ADK, and Cognee GraphRAG configurations.
"""

import os
from typing import Optional, List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

# Load environment variables
load_dotenv()

class A2AServerConfig(BaseSettings):
    """A2A Server configuration"""
    host: str = Field(default="localhost", env="A2A_SERVER_HOST")
    port: int = Field(default=8080, env="A2A_SERVER_PORT")
    network_mode: str = Field(default="development", env="A2A_NETWORK_MODE")
    protocol_version: str = Field(default="1.0", env="A2A_PROTOCOL_VERSION")
    max_concurrent_requests: int = Field(default=100, env="A2A_MAX_CONCURRENT_REQUESTS")
    request_timeout: int = Field(default=30, env="A2A_REQUEST_TIMEOUT")
    
    # Security
    tls_enabled: bool = Field(default=False, env="A2A_TLS_ENABLED")
    tls_cert_file: Optional[str] = Field(default=None, env="A2A_TLS_CERT_FILE")
    tls_key_file: Optional[str] = Field(default=None, env="A2A_TLS_KEY_FILE")
    api_key_secret: Optional[str] = Field(default=None, env="A2A_AGENT_API_KEY_SECRET")
    network_secret: Optional[str] = Field(default=None, env="A2A_NETWORK_SECRET")
    
    # Monitoring
    enable_metrics: bool = Field(default=True, env="A2A_ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="A2A_METRICS_PORT")

class GoogleCloudConfig(BaseSettings):
    """Google Cloud and ADK configuration"""
    project_id: Optional[str] = Field(default=None, env="GOOGLE_CLOUD_PROJECT")
    vertex_ai_location: str = Field(default="us-central1", env="VERTEX_AI_LOCATION")
    credentials_path: Optional[str] = Field(default=None, env="GOOGLE_APPLICATION_CREDENTIALS")
    
    # ADK Configuration
    model: str = Field(default="gemini-2.0-flash", env="ADK_MODEL")
    log_level: str = Field(default="INFO", env="ADK_LOG_LEVEL")

class MCPConfig(BaseSettings):
    """MCP Server configuration"""
    server_url: str = Field(default="http://127.0.0.1:8000/sse", env="MCP_SERVER_URL")
    timeout: int = Field(default=30, env="MCP_SERVER_TIMEOUT")

class CogneeConfig(BaseSettings):
    """Cognee GraphRAG configuration"""
    llm_api_key: Optional[str] = Field(default=None, env="LLM_API_KEY")
    vector_db_provider: str = Field(default="lancedb", env="VECTOR_DB_PROVIDER")
    graph_database_provider: str = Field(default="neo4j", env="GRAPH_DATABASE_PROVIDER")
    db_provider: str = Field(default="sqlite", env="DB_PROVIDER")
    
    # Neo4j Configuration
    graph_database_url: str = Field(default="bolt://localhost:7687", env="GRAPH_DATABASE_URL")
    graph_database_username: str = Field(default="neo4j", env="GRAPH_DATABASE_USERNAME")
    graph_database_password: str = Field(default="password123", env="GRAPH_DATABASE_PASSWORD")
    
    # Embedding Configuration
    embedding_provider: str = Field(default="fastembed", env="EMBEDDING_PROVIDER")
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", env="EMBEDDING_MODEL")
    embedding_dimensions: int = Field(default=384, env="EMBEDDING_DIMENSIONS")
    embedding_max_tokens: int = Field(default=256, env="EMBEDDING_MAX_TOKENS")

class NotificationConfig(BaseSettings):
    """Notification system configuration"""
    threshold: float = Field(default=0.7, env="NOTIFICATION_THRESHOLD")
    channels: List[str] = Field(default=["console", "file"], env="NOTIFICATION_CHANNELS")
    webhook_url: Optional[str] = Field(default=None, env="WEBHOOK_URL")

class SystemConfig(BaseSettings):
    """Main system configuration combining all components"""
    env: str = Field(default="development", env="ENV")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create config instances using object.__setattr__ to avoid Pydantic validation
        object.__setattr__(self, 'a2a', A2AServerConfig())
        object.__setattr__(self, 'google_cloud', GoogleCloudConfig())
        object.__setattr__(self, 'mcp', MCPConfig())
        object.__setattr__(self, 'cognee', CogneeConfig())
        object.__setattr__(self, 'notifications', NotificationConfig())
    
    def validate_config(self) -> bool:
        """Validate all configuration settings"""
        errors = []
        
        # Google Cloud settings are optional for local mode
        # if not self.google_cloud.project_id:
        #     errors.append("GOOGLE_CLOUD_PROJECT is required")
        
        # Check required API keys
        if not self.cognee.llm_api_key:
            errors.append("LLM_API_KEY is required")
        
        # Check TLS configuration
        if self.a2a.tls_enabled and (not self.a2a.tls_cert_file or not self.a2a.tls_key_file):
            errors.append("TLS certificate and key files required when TLS is enabled")
        
        if errors:
            for error in errors:
                print(f"Configuration error: {error}")
            return False
        
        return True

# Global configuration instance
config = SystemConfig()