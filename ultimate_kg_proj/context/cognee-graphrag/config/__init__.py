"""Configuration helpers for Cognee MCP server setup."""

from .mcp_env_setup import (
    create_mcp_env_file,
    create_claude_settings,
    validate_environment,
    print_setup_status,
    setup_interactive
)

# Legacy database configs kept for reference
from .neo4j import Neo4jConfig, get_neo4j_config
from .lancedb import LanceDBConfig, get_lancedb_config  
from .sqlite import SQLiteConfig, get_sqlite_config

__all__ = [
    # MCP setup functions
    'create_mcp_env_file',
    'create_claude_settings', 
    'validate_environment',
    'print_setup_status',
    'setup_interactive',
    
    # Legacy database configs (for reference)
    'Neo4jConfig',
    'LanceDBConfig',
    'SQLiteConfig',
    'get_neo4j_config',
    'get_lancedb_config',
    'get_sqlite_config',
]


def setup_mcp_environment(cognee_mcp_path, api_key, **kwargs):
    """Setup MCP server environment with database configuration."""
    print("🔧 Setting up Cognee MCP server environment...")
    
    # Create environment file
    env_success = create_mcp_env_file(cognee_mcp_path, api_key, **kwargs)
    
    # Create Claude settings
    settings_path = create_claude_settings(cognee_mcp_path)
    
    # Validate setup
    validation_results = validate_environment(cognee_mcp_path)
    
    return {
        'env_file_created': env_success,
        'settings_file': settings_path,
        'validation': validation_results,
        'setup_complete': all(validation_results.values())
    }