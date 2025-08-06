# Agentic GraphRAG System with A2A Protocol Integration

A comprehensive multi-agent system that integrates Google ADK agents with Cognee GraphRAG via A2A Protocol endpoints for knowledge ingestion, fact extraction, and connection discovery.

## Overview

This system combines three major technologies:
- **A2A Protocol**: Standardized agent-to-agent communication
- **Google ADK**: Multi-agent coordination and orchestration  
- **Cognee GraphRAG**: Multi-database knowledge graph operations (Neo4j + LanceDB + SQLite)

## Architecture

```
External Systems → A2A Server → KG Agent (ADK) → Cognee GraphRAG
                                    ↓
                            Fact Extraction Pipeline
                                    ↓  
                            Connection Detection
                                    ↓
                            Notification System
```

## Quick Start

### 1. Environment Setup

```bash
# Copy environment configuration
cp .env.example .env

# Edit .env with your configuration
# - Set GOOGLE_CLOUD_PROJECT
# - Set LLM_API_KEY
# - Configure database connections
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Infrastructure

```bash
# Start Neo4j database
docker run -d \
  --name neo4j-agentic \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password123 \
  neo4j:latest

# Start Cognee MCP server
cd ../context/cognee-graphrag
python examples/mcp_server_setup.py
```

### 4. Run the System

```bash
# Start A2A server
python main.py

# Test the system
curl -X POST http://localhost:8080/agents/kg_ingest \
  -H "Content-Type: application/json" \
  -d '{"data": "Sample text to process"}'
```

## Components

### A2A Server (`server/`)
- RESTful endpoints for external system integration
- A2A protocol compliance and validation
- Request routing to appropriate agents

### KG Agent (`agents/kg_agent.py`)
- Google ADK agent with MCP toolset integration
- Cognee GraphRAG operations coordination
- Multi-agent workflow orchestration

### Fact Extraction Pipeline (`agents/extraction/`)
- Document processor for files (PDF, Word, text)
- Chat processor for conversational data
- Structured data processor for JSON/CSV
- Parallel processing coordination

### Connection Detection (`agents/connection_detector.py`)
- Semantic similarity analysis using LanceDB
- Graph relationship traversal via Neo4j
- Relevance scoring and threshold management

### Notification System (`agents/notification_manager.py`)
- Multi-channel alerts (console, file, webhook)
- Configurable notification triggers
- User preference management

## API Endpoints

### Knowledge Ingestion
```bash
POST /agents/kg_ingest
{
  "data": "Text or structured data to process",
  "format": "text|json|pdf|csv",
  "options": {
    "extract_facts": true,
    "detect_connections": true,
    "notify_threshold": 0.7
  }
}
```

### Knowledge Search
```bash
POST /agents/kg_search
{
  "query": "Search query",
  "type": "semantic|graph|hybrid",
  "limit": 10
}
```

### System Status
```bash
GET /agents/kg_status
```

## Configuration

The system uses environment variables for configuration. Key settings:

### A2A Server
- `A2A_SERVER_PORT`: Server port (default: 8080)
- `A2A_MAX_CONCURRENT_REQUESTS`: Request limit (default: 100)

### Google Cloud
- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID
- `VERTEX_AI_LOCATION`: Vertex AI region (default: us-central1)
- `ADK_MODEL`: Model to use (default: gemini-2.0-flash)

### Cognee GraphRAG
- `LLM_API_KEY`: Required API key for language models
- `GRAPH_DATABASE_URL`: Neo4j connection (default: bolt://localhost:7687)
- `MCP_SERVER_URL`: MCP server endpoint

### Notifications
- `NOTIFICATION_THRESHOLD`: Relevance threshold (default: 0.7)
- `NOTIFICATION_CHANNELS`: Alert channels (default: console,file)

## Testing

```bash
# Run unit tests
pytest tests/ -v

# Run integration tests
pytest tests/integration/ -v

# Test A2A protocol compliance
a2a-validator --server-url http://localhost:8080

# Run performance tests
pytest tests/performance/ -v
```

## Deployment

### Development
```bash
python main.py
```

### Production (Docker)
```bash
docker build -t agentic-graphrag .
docker run -p 8080:8080 --env-file .env agentic-graphrag
```

### Google Cloud Run
```bash
gcloud run deploy agentic-graphrag \
  --source . \
  --region us-central1 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=your-project
```

## Validation

The system includes comprehensive validation:

1. **Component Tests**: Individual agent and service testing
2. **Integration Tests**: End-to-end workflow validation  
3. **A2A Protocol Tests**: Standards compliance verification
4. **Performance Tests**: Concurrent request handling

## Troubleshooting

### Common Issues

1. **MCP Server Connection**: Ensure Cognee MCP server is running
2. **Neo4j Connection**: Verify database is accessible at configured URL
3. **Google Cloud Auth**: Check service account credentials
4. **A2A Protocol**: Validate configuration with a2a-validator

### Debug Mode
```bash
# Enable debug logging
export ADK_LOG_LEVEL=DEBUG
export A2A_LOG_LEVEL=DEBUG
python main.py
```

## Contributing

1. Follow existing code patterns from reference implementations
2. Add tests for new functionality
3. Validate A2A protocol compliance
4. Update documentation

## License

See LICENSE file for details.