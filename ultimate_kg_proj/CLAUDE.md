# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Architecture

This is a multi-project repository containing major knowledge graph and AI agent development frameworks:

### cognee-graphrag/
MCP (Model Context Protocol) server implementation using Cognee for multi-database GraphRAG with Neo4j, LanceDB, and SQLite. Designed for seamless Claude Code integration through MCP tools.

**Core Architecture:**
- **MCP Server**: Provides `cognify`, `search`, `codify`, `list_data`, `delete`, `prune` tools to Claude Code
- **Multi-Database**: Neo4j (graph), LanceDB (vectors), SQLite (metadata) working in coordination
- **Knowledge Processing**: Document → Entity extraction → Multi-database storage → Semantic search

### google-adk/
Google Agent Development Kit templates and examples for building production-grade AI agents and multi-agent systems.

**Core Architecture:**
- **Multi-Agent Coordination**: Hierarchical agent systems with specialized roles
- **Google Cloud Integration**: Vertex AI, Cloud Run deployment patterns
- **PRP Methodology**: Product Requirements Prompts for systematic agent development

### a2a-google-adk/
A2A (Agent-to-Agent) protocol compatible AI agents using Google's Agent Development Kit with cross-platform interoperability. Located at `C:\projects\ultimate_kg\ultimate_kg_proj\a2a-google-adk`.

**Core Architecture:**
- **A2A Protocol Compliance**: Full adherence to Agent-to-Agent protocol specifications for cross-platform communication
- **Cross-Platform Interoperability**: Seamless communication with LangGraph, CrewAI, Semantic Kernel agents
- **Google ADK Integration**: Vertex AI models and tools within A2A framework
- **Agent Network Coordination**: Distributed agent systems across multiple platforms

## Development Commands

### cognee-graphrag/ Commands
```bash
# Install dependencies
pip install -e ".[dev]"

# Code quality
black .                    # Format code
ruff check .              # Lint code  
ruff check . --fix        # Fix lint issues
mypy .                    # Type checking

# Testing
pytest                    # Run all tests
pytest tests/specific_test.py  # Run specific test
pytest -v                 # Verbose output
pytest -k "test_name"     # Run tests matching pattern

# Database setup
docker-compose up neo4j    # Start Neo4j only
docker-compose up         # Start all databases (Neo4j, Redis, PostgreSQL, Qdrant)
python examples/mcp_server_setup.py  # Complete MCP setup automation

# MCP Server
python examples/mcp_server_setup.py  # Automated setup
cd cognee-mcp && uv run src/server.py  # Manual server start
```

### google-adk/ Commands
```bash
# Agent development workflow
python copy_template.py /path/to/new-project  # Copy template
python examples/basic_chat_agent/agent.py     # Run basic agent
python examples/multi_agent_system/coordinator.py  # Multi-agent system

# Environment setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Configure with API keys

# Testing agent systems
python examples/*/run_agent.py  # Test individual agents
pytest tests/ -v              # Run agent tests if available
```

### a2a-google-adk/ Commands
```bash
# A2A server setup and agent development
python copy_template.py /path/to/new-a2a-project  # Copy A2A template
python config/a2a_server_config.py --validate     # Validate A2A configuration
python examples/basic_a2a_agent/agent.py          # Run basic A2A-compatible agent

# A2A protocol compliance and testing
pip install a2a-sdk[grpc,telemetry]               # Install A2A SDK
pip install google-adk google-cloud-aiplatform    # Install Google ADK dependencies
a2a-validator --server-url http://localhost:8080  # Validate A2A protocol compliance

# Cross-platform agent coordination
python examples/cross_platform_delegation/test_delegation.py  # Test cross-platform delegation
python examples/multi_agent_coordination/coordinator.py       # Multi-platform coordination
python examples/a2a_testing_framework/test_compliance.py      # A2A compliance testing

# Google Cloud deployment
gcloud auth application-default login              # Authenticate with Google Cloud
gcloud run deploy --source . --region us-central1 # Deploy A2A server to Cloud Run
```

## Key Integration Workflows

### MCP Server Integration with Claude Code
1. **Setup**: Use `examples/mcp_server_setup.py` for complete automation
2. **Configuration**: Copy settings from `settings.json.example` to Claude Code settings
3. **Database Stack**: Start with `docker-compose up neo4j` for basic setup
4. **Validation**: Test MCP tools availability in Claude Code: "List available MCP tools"

### Agent Development with PRP Framework
1. **Requirements**: Define in `PRPs/INITIAL.md` 
2. **Generate Plan**: `/generate-google-adk-prp PRPs/INITIAL.md`
3. **Execute**: `/execute-google-adk-prp PRPs/generated-prp.md`
4. **Deploy**: Use `examples/cloud_run_deployment/` patterns

## Database Configuration Patterns

### Multi-Database GraphRAG (cognee-graphrag/)
- **Neo4j**: Knowledge graph storage (`config/neo4j.py`)
- **LanceDB**: Vector embeddings (`config/lancedb.py`) 
- **SQLite**: Metadata and status (`config/sqlite.py`)
- **Unified Interface**: `config/__init__.py` provides consistent database access

### Environment Configuration
```bash
# cognee-graphrag/.env pattern
LLM_API_KEY=your_key
GRAPH_DATABASE_PROVIDER=neo4j
VECTOR_DB_PROVIDER=lancedb
DB_PROVIDER=sqlite
GRAPH_DATABASE_URL=bolt://localhost:7687
GRAPH_DATABASE_USERNAME=neo4j
GRAPH_DATABASE_PASSWORD=password123

# google-adk/.env pattern  
ADK_MODEL=gemini-2.0-flash
GOOGLE_CLOUD_PROJECT=your-project
VERTEX_AI_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

## Agent Architecture Patterns

### MCP Tool Integration (cognee-graphrag/)
- **Document Processing**: `cognify` tool processes documents into knowledge graphs
- **Semantic Search**: `search` tool queries across all databases (vector + graph + relational)
- **Code Analysis**: `codify` tool analyzes repositories for dependency mapping
- **Knowledge Management**: `list_data`, `delete`, `prune` for data lifecycle

### Multi-Agent Coordination (google-adk/)
- **Hierarchical**: Parent coordinator with specialized sub-agents
- **Sequential**: Step-by-step workflow processing with state management
- **Parallel**: Concurrent task execution with result aggregation
- **Tool Integration**: Built-in tools (google_search, code_execution) + custom tools

## Production Deployment

### MCP Server Deployment
- **Container**: Use docker-compose.yml for database infrastructure
- **MCP Integration**: Configure Claude Code settings.json with proper cwd paths
- **Scaling**: Neo4j memory configuration, LanceDB optimization
- **Monitoring**: Database health checks, MCP server status validation

### Google Cloud Agent Deployment  
```bash
# Cloud Run deployment
docker build -t agent-system .
gcloud run deploy --image agent-system --region us-central1

# Vertex AI integration
# Configure service accounts and IAM roles
# Set regional endpoints for model availability
# Implement cost controls and quotas
```

## Common Troubleshooting

### MCP Server Issues
- **Database Connections**: Check docker containers with `docker ps`
- **Environment Variables**: Verify `.env` file configuration
- **Claude Code Integration**: Ensure `cwd` in settings.json points to cognee-mcp directory
- **API Keys**: Validate LLM_API_KEY is properly set

### Agent Development Issues
- **Google Cloud Auth**: Verify service account setup and IAM roles
- **Model Availability**: Different models available in different regions
- **Agent Coordination**: Keep hierarchies simple, avoid over-complex delegation
- **Cost Management**: Monitor token usage, set appropriate quotas

### Database Setup Issues
```bash
# Reset databases
docker-compose down -v  # Remove volumes
docker-compose up neo4j # Restart clean

# Check connections
docker logs neo4j-cognee
telnet localhost 7687  # Test Neo4j connection
```

## Important File Relationships

### cognee-graphrag/ Dependencies
- `examples/mcp_server_setup.py` orchestrates complete system setup
- `config/mcp_env_setup.py` generates environment configuration  
- `docker-compose.yml` provides database infrastructure
- `settings.json.example` configures Claude Code MCP integration
- `workflows/*.md` document agent usage patterns

### google-adk/ Dependencies  
- `copy_template.py` deploys project templates
- `PRPs/templates/prp_google_adk_base.md` provides systematic development framework
- `examples/*/agent.py` demonstrate multi-agent coordination patterns
- `CLAUDE.md` contains Google ADK-specific development rules

This repository enables building sophisticated knowledge graph systems with MCP integration and production-grade multi-agent systems using Google's ADK framework.