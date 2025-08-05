# Cognee MCP GraphRAG Use Case Directory

This directory contains a complete implementation for building MCP-based agentic systems using Cognee with multi-database GraphRAG architecture (Neo4j + LanceDB + SQLite).

## Directory Structure & Implementation Guide

```
cognee-graphrag/
├── config/                    # Database configuration & MCP setup
├── examples/                  # Working implementations & patterns
├── workflows/                 # Agent workflow documentation  
├── src/                      # Legacy GraphRAG implementation (reference)
├── docker-compose.yml        # Multi-database orchestration
├── settings.json.example     # Claude Code MCP configuration
└── .env.example             # MCP server environment template
```

## Core Implementation Files

### MCP Server Configuration
- **`config/mcp_env_setup.py`** - Main MCP environment configuration helper
- **`settings.json.example`** - Claude Code MCP server integration template
- **`.env.example`** - Cognee MCP server environment variables template
- **`docker-compose.yml`** - Neo4j + optional databases setup
- **`docker-compose.minimal.yml`** - Neo4j-only setup for basic usage

### Database Configuration Files
- **`config/neo4j.py`** - Neo4j connection management & graph database setup
- **`config/lancedb.py`** - LanceDB vector database configuration  
- **`config/sqlite.py`** - SQLite relational database setup
- **`config/__init__.py`** - Unified database configuration interface

### Working Examples & Patterns
- **`examples/mcp_server_setup.py`** - Complete automated MCP server setup script
- **`examples/claude_workflows.py`** - MCP tool usage patterns & workflow examples
- **`examples/basic_setup.py`** - MCP integration testing & validation
- **`examples/document_processing.py`** - Document workflow examples (legacy reference)
- **`examples/graphrag_queries.py`** - Advanced query patterns (legacy reference)

### Agent Workflow Documentation
- **`workflows/research_workflow.md`** - Research paper analysis workflow
- **`workflows/document_analysis.md`** - Business document processing workflow  
- **`workflows/knowledge_extraction.md`** - Advanced knowledge synthesis patterns

## Cognee MCP Tools Reference

When using this setup, agents can access these Cognee MCP tools:

### Core Processing Tools
- **`cognify`** - Process documents/data into knowledge graphs (stores in Neo4j + LanceDB)
- **`search`** - Query knowledge base (vector similarity, graph traversal, combined search)
- **`codify`** - Analyze code repositories & extract dependencies

### Management Tools  
- **`list_data`** - Show processed datasets & status
- **`delete`** - Remove specific data entries
- **`prune`** - Reset entire knowledge base

## Implementation Workflow for Agents

### 1. Environment Setup
**Primary file: `examples/mcp_server_setup.py`**
- Automated Cognee MCP server installation
- Database configuration & Docker setup  
- Environment file generation
- Validation & testing

**Configuration files:**
- Copy `.env.example` → `cognee-mcp/.env` with your API keys
- Use `settings.json.example` for Claude Code MCP integration
- Run `docker-compose up neo4j` for graph database

### 2. Database Architecture Implementation
**Neo4j (Graph Database):**
- File: `config/neo4j.py` - Connection management & indexing
- Stores: Entities, relationships, knowledge graph structure
- Usage: Complex queries, relationship traversal, graph analytics

**LanceDB (Vector Database):**  
- File: `config/lancedb.py` - Vector storage configuration
- Stores: Document embeddings, semantic similarity data
- Usage: Fast similarity search, content clustering

**SQLite (Metadata):**
- File: `config/sqlite.py` - Relational data management  
- Stores: Processing status, document metadata, audit logs
- Usage: Structured queries, status tracking, configuration

### 3. MCP Server Integration Patterns
**For Agent Development:**
```python
# See examples/claude_workflows.py for complete patterns
# MCP tools available through HTTP/stdio transport:
# - cognify: Document → Knowledge Graph
# - search: Query across all databases  
# - codify: Code analysis & dependency mapping
```

### 4. Agent Workflow References
**Research Workflows:** `workflows/research_workflow.md`
- Multi-document synthesis patterns
- Citation & relationship mapping
- Temporal analysis workflows

**Business Intelligence:** `workflows/document_analysis.md`  
- Entity extraction from business documents
- Stakeholder mapping & analysis
- Compliance & risk assessment patterns

**Knowledge Engineering:** `workflows/knowledge_extraction.md`
- Cross-domain knowledge synthesis  
- Automated relationship discovery
- Knowledge gap analysis

## Quick Start for Agent Implementation

1. **Setup**: Run `python examples/mcp_server_setup.py` for automated configuration
2. **Test**: Use `python examples/basic_setup.py` to validate MCP integration  
3. **Deploy**: Use `docker-compose up` for production database stack
4. **Integrate**: Copy `settings.json.example` configuration for MCP client setup

## File Dependencies & Relationships

- `config/mcp_env_setup.py` → Generates → `.env` file for MCP server
- `docker-compose.yml` → Provides → Database infrastructure  
- `examples/mcp_server_setup.py` → Orchestrates → Complete system setup
- `workflows/*.md` → Document → Agent usage patterns
- `settings.json.example` → Configures → MCP client integration

This directory provides everything needed to build production-ready MCP-based agentic systems with GraphRAG capabilities.