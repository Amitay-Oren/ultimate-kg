# Cognee MCP Server with Multi-Database GraphRAG

A complete MCP (Model Context Protocol) server setup using Cognee for GraphRAG with Neo4j, LanceDB, and SQLite. Designed for seamless Claude Code integration.

## 🏗️ Architecture

```
                    ┌─────────────────┐
                    │   Claude Code   │
                    │  (Your AI IDE)  │
                    └─────────────────┘
                                 │ MCP Protocol
                    ┌─────────────────┐
                    │  Cognee MCP     │
                    │    Server       │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Neo4j       │    │    LanceDB      │    │     SQLite      │
│  (Knowledge     │    │   (Vector       │    │  (Relational    │
│   Graph)        │    │    Search)      │    │   Metadata)     │
│                 │    │                 │    │                 │
│ • Entities      │    │ • Embeddings    │    │ • Documents     │
│ • Relationships │    │ • Similarity    │    │ • Status        │
│ • Graph Queries │    │ • Semantic      │    │ • Audit Logs    │
│                 │    │   Search        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) - Your AI IDE
- Python 3.9+ - For running the MCP server
- [UV](https://docs.astral.sh/uv/) - Fast Python package management
- Docker - For Neo4j database
- OpenAI API Key - For embeddings and LLM operations

### 1. Clone and Setup Cognee MCP Server

```bash
# Clone Cognee repository
git clone https://github.com/topoteretes/cognee.git
cd cognee/cognee-mcp

# Install dependencies
uv sync --dev --all-extras
```

### 2. Database Setup

#### Neo4j (Knowledge Graph)
```bash
# Start Neo4j with Docker
docker run -d \
  --name neo4j-cognee \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password123 \
  neo4j:latest
```

#### LanceDB & SQLite
```bash
# These run embedded within the MCP server
# LanceDB: High-performance vector storage
# SQLite: Lightweight relational database
# No separate setup required
```

### 3. Configure MCP Server Environment

```bash
# In the cognee-mcp directory
cp .env.example .env
```

Edit `.env` with your database preferences:
```env
# Required: LLM API Key
LLM_API_KEY=your_openai_key_here

# Database Providers
VECTOR_DB_PROVIDER=lancedb
GRAPH_DATABASE_PROVIDER=neo4j
DB_PROVIDER=sqlite

# Neo4j Configuration (if using)
GRAPH_DATABASE_URL=bolt://localhost:7687
GRAPH_DATABASE_USERNAME=neo4j
GRAPH_DATABASE_PASSWORD=password123

# Optional: Embedding Configuration
EMBEDDING_PROVIDER=fastembed
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSIONS=384
```

### 4. Start the MCP Server

```bash
# Start the server (from cognee-mcp directory)
uv run src/server.py

# Server will:
# ✅ Run database migrations
# ✅ Initialize default user
# ✅ Start MCP server on stdio
```

### 5. Configure Claude Code

Add to your Claude Code `settings.json`:
```json
{
  "mcpServers": {
    "cognee": {
      "command": "uv",
      "args": ["run", "python", "src/server.py"],
      "cwd": "/path/to/cognee/cognee-mcp",
      "env": {
        "LLM_API_KEY": "your_openai_key_here"
      }
    }
  }
}
```

### 6. Verify Integration

Open Claude Code and test MCP tools:
```
List available MCP tools
# Should show: cognify, search, codify, list_data, delete, prune
```

## 📊 Database Roles

### Neo4j (Knowledge Graph)
- **Purpose**: Store entities, relationships, and semantic connections
- **Use Cases**: 
  - Entity relationship mapping
  - Graph traversal queries
  - Knowledge discovery
  - Relationship inference

### LanceDB (Vector Search)
- **Purpose**: Fast semantic similarity search
- **Use Cases**:
  - Document similarity
  - Entity embedding search
  - Semantic retrieval
  - Clustering analysis

### SQLite (Relational)
- **Purpose**: Metadata and structured data
- **Use Cases**:
  - Document metadata
  - Processing status
  - Configuration data
  - Audit logs

## 🔧 Claude Code Workflows

### Basic Document Processing

In Claude Code, use these MCP tools:

```
# 1. Add documents to Cognee
Use the 'cognify' tool to process your documents:
- Specify document path or content
- Cognee will extract entities and relationships
- Data stored across Neo4j, LanceDB, and SQLite

# 2. Search your knowledge base
Use the 'search' tool for queries:
- Vector search: Semantic similarity
- Graph search: Relationship traversal  
- Combined search: Best of both approaches
```

### Example Claude Conversations

**Document Analysis:**
```
You: "Process the documents in ./research_papers/ using cognify"
Claude: [Uses cognify tool to process documents]
You: "What are the main concepts about machine learning?"
Claude: [Uses search tool to find relevant information]
```

**Knowledge Extraction:**
```
You: "Search for connections between AI researchers and their contributions"
Claude: [Uses search with graph traversal to find relationships]
You: "Show me the research timeline"
Claude: [Combines multiple search results to build timeline]
```

## 🛠️ MCP Tools Available

Claude Code can use these Cognee tools:

- **`cognify`** - Process documents/data into knowledge graph
  - Extracts entities and relationships
  - Stores embeddings in LanceDB
  - Creates graph structure in Neo4j

- **`search`** - Query knowledge base across all databases
  - Vector similarity search
  - Graph relationship queries
  - Combined multi-modal search

- **`codify`** - Analyze code repositories
  - Extract code structure and dependencies
  - Create code knowledge graphs

- **`list_data`** - Show available datasets and status
- **`delete`** - Remove specific data entries
- **`prune`** - Reset entire knowledge base

## 📁 Use Case Structure

This use case provides templates and examples for MCP setup:

```
cognee-mcp/
├── CLAUDE.md                 # Claude Code MCP instructions
├── README.md                 # Setup and workflow guide
├── docker-compose.yml        # Multi-database setup
├── settings.json.example     # Claude Code MCP configuration
├── .env.example             # MCP server environment
├── config/                  # Database setup helpers
│   ├── mcp_env_setup.py    # Environment configuration
│   ├── database_init.py    # Database initialization
│   └── neo4j_setup.py      # Neo4j specific setup
├── examples/                # MCP workflow examples
│   ├── mcp_server_setup.py # Complete MCP setup
│   ├── claude_workflows.py # Claude usage patterns
│   └── troubleshooting.py  # Common issues & solutions
├── workflows/               # Claude workflow guides
│   ├── research_workflow.md
│   ├── document_analysis.md
│   └── knowledge_extraction.md
└── PRPs/                   # Requirements & planning
    └── INITIAL_MCP.md      # Updated requirements
```

## 🔍 Key Features

- **MCP-First Design**: Built specifically for Claude Code integration
- **Multi-Database GraphRAG**: Neo4j + LanceDB + SQLite working together
- **One-Command Setup**: Simple MCP server configuration
- **Real Workflows**: Practical Claude Code usage patterns
- **Database Flexibility**: Configure your preferred database stack
- **Production Ready**: Handles migrations, users, and scaling

## 🚨 Troubleshooting

### MCP Server Won't Start
```bash
# Check environment variables
cat .env

# Verify dependencies
uv sync --dev --all-extras

# Test with minimal config
LLM_API_KEY=your_key uv run src/server.py
```

### Claude Code Can't Find Tools
```bash
# Verify MCP server is running
ps aux | grep server.py

# Check Claude Code settings.json path
# Ensure "cwd" points to cognee-mcp directory
```

### Database Connection Issues
```bash
# Test Neo4j connection
docker logs neo4j-cognee

# Check if port 7687 is accessible
telnet localhost 7687
```

### Reset Everything
```bash
# Stop MCP server, clear databases, restart
docker restart neo4j-cognee
rm -rf ./lancedb_data/ ./cognee.db
uv run src/server.py
```

## 📚 Further Reading

- [Cognee MCP Server](https://github.com/topoteretes/cognee/tree/main/cognee-mcp)
- [Cognee Documentation](https://docs.cognee.ai/)
- [Claude Code MCP Guide](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Neo4j Setup Guide](https://neo4j.com/docs/operations-manual/current/installation/)

## 🎯 Next Steps

1. **Basic Setup**: Follow the quick start guide above
2. **Test Integration**: Verify MCP tools work in Claude Code  
3. **Process Documents**: Use `cognify` to build your knowledge base
4. **Explore Workflows**: Try the example workflows in `workflows/`
5. **Customize**: Adapt database and embedding configurations

## 📄 License

MIT License - This use case template is free to use and modify.