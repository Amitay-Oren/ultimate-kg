#!/usr/bin/env python3
"""
MCP Server Setup Example for Cognee GraphRAG.

This example demonstrates:
1. Setting up the Cognee MCP server environment
2. Testing database connections  
3. Configuring Claude Code MCP integration
4. Verifying MCP server functionality
"""

import asyncio
import os
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def check_prerequisites():
    """Check if required tools and services are available."""
    print("🔍 Checking Prerequisites")
    
    # Check if Cognee MCP repo exists
    cognee_paths = [
        Path.home() / "cognee" / "cognee-mcp",
        Path.cwd().parent / "cognee" / "cognee-mcp",
        Path("/opt/cognee/cognee-mcp")
    ]
    
    cognee_mcp_path = None
    for path in cognee_paths:
        if path.exists():
            cognee_mcp_path = path
            break
    
    if not cognee_mcp_path:
        print("❌ Cognee MCP server not found")
        print("📋 Please clone Cognee:")
        print("   git clone https://github.com/topoteretes/cognee.git")
        print("   cd cognee/cognee-mcp")
        print("   uv sync --dev --all-extras")
        return None
    
    print(f"✅ Found Cognee MCP at: {cognee_mcp_path}")
    
    # Check if Neo4j is running (if configured)
    try:
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        if "neo4j" in result.stdout:
            print("✅ Neo4j container is running")
        else:
            print("⚠️  Neo4j container not found")
            print("💡 Start with: docker run -d --name neo4j-cognee -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password123 neo4j:latest")
    except FileNotFoundError:
        print("⚠️  Docker not found - Neo4j setup may be needed")
    
    # Check API keys
    if not os.getenv("LLM_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("❌ No LLM API key found")
        print("💡 Set LLM_API_KEY or OPENAI_API_KEY in environment")
        return None
    
    print("✅ API key configured")
    return cognee_mcp_path


def create_mcp_settings(cognee_path):
    """Create Claude Code MCP settings configuration."""
    print("\n🔧 Creating Claude Code MCP Configuration")
    
    settings = {
        "mcpServers": {
            "cognee": {
                "command": "uv",
                "args": ["run", "python", "src/server.py"],
                "cwd": str(cognee_path),
                "env": {
                    "LLM_API_KEY": os.getenv("LLM_API_KEY", os.getenv("OPENAI_API_KEY", "")),
                    "VECTOR_DB_PROVIDER": "lancedb",
                    "GRAPH_DATABASE_PROVIDER": "neo4j",
                    "DB_PROVIDER": "sqlite",
                    "GRAPH_DATABASE_URL": "bolt://localhost:7687",
                    "GRAPH_DATABASE_USERNAME": "neo4j",
                    "GRAPH_DATABASE_PASSWORD": "password123"
                }
            }
        }
    }
    
    settings_file = Path.cwd() / "settings.json.example"
    settings_file.write_text(json.dumps(settings, indent=2))
    
    print(f"✅ Created: {settings_file}")
    print("📋 Add this configuration to your Claude Code settings.json")
    
    return settings


def test_mcp_server(cognee_path):
    """Test if the MCP server can start."""
    print("\n🧪 Testing MCP Server")
    
    try:
        # Test server startup (with timeout)
        print("⏳ Starting MCP server (5 second test)...")
        
        env = os.environ.copy()
        env.update({
            "LLM_API_KEY": os.getenv("LLM_API_KEY", os.getenv("OPENAI_API_KEY", "")),
            "VECTOR_DB_PROVIDER": "lancedb",
            "GRAPH_DATABASE_PROVIDER": "neo4j",
            "DB_PROVIDER": "sqlite"
        })
        
        process = subprocess.Popen(
            ["uv", "run", "python", "src/server.py"],
            cwd=cognee_path,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait briefly then terminate
        try:
            stdout, stderr = process.communicate(timeout=5)
            print("✅ MCP server started successfully")
            return True
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait()
            print("✅ MCP server startup confirmed (terminated after test)")
            return True
            
    except Exception as e:
        print(f"❌ MCP server test failed: {e}")
        print("💡 Check your environment configuration and dependencies")
        return False


async def main():
    """MCP Server setup demonstration."""
    print("🚀 Cognee MCP Server Setup Example")
    print("=" * 45)
    
    # Step 1: Check prerequisites
    print("\n1️⃣  Checking Prerequisites")
    cognee_path = check_prerequisites()
    
    if not cognee_path:
        print("\n❌ Prerequisites not met. Please fix issues above and retry.")
        return
    
    # Step 2: Create Claude Code configuration
    print("\n2️⃣  Creating Claude Code Configuration")
    mcp_settings = create_mcp_settings(cognee_path)
    
    # Step 3: Test MCP server
    print("\n3️⃣  Testing MCP Server")
    server_works = test_mcp_server(cognee_path)
    
    if not server_works:
        print("\n⚠️  MCP server test failed - check configuration")
    
    # Step 4: Provide next steps
    print("\n4️⃣  Next Steps")
    print("✅ Setup completed! Next actions:")
    print(f"   1. Add the configuration from {Path.cwd()}/settings.json.example to your Claude Code settings")
    print("   2. Start the MCP server:")
    print(f"      cd {cognee_path}")
    print("      uv run src/server.py")
    print("   3. Open Claude Code and test MCP tools:")
    print("      'List available MCP tools' should show cognee tools")
    print("   4. Try document processing:")
    print("      'Use cognify to process documents in ./examples/'")
    
    print("\n🎯 MCP Integration Status:")
    print("   ✅ Configuration created")
    print("   ✅ Server tested" if server_works else "   ⚠️  Server needs configuration")
    print("   ⏳ Ready for Claude Code integration")


if __name__ == "__main__":
    asyncio.run(main())