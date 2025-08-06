# Graphiti Agent API - Quick Start Guide

A simple HTTP API wrapper for querying your Graphiti knowledge graph. Perfect for Claude Code integration!

## 🚀 Quick Start

### Step 1: Start Your Graphiti MCP Server
```bash
cd "C:\Users\Amitay Oren\graphiti\mcp_server"
uv run graphiti_mcp_server.py
```
Wait until you see: `Uvicorn running on http://127.0.0.1:8000`

### Step 2: Start the API (Choose One Method)

#### Option A: Docker (Recommended)
```bash
cd /path/to/a2a-agents
docker-compose up --build
```

#### Option B: Python Directly
```bash
cd async-a2a
python api_server.py
```

### Step 3: Test It Works
```bash
curl http://localhost:8080/health
```

Should return: `{"status": "healthy"}`

## 💬 Usage Examples

### For Claude Code
```bash
# Ask about the user
curl "http://localhost:8080/query?q=What+do+you+know+about+the+user"

# Ask about hobbies
curl "http://localhost:8080/query?q=Tell+me+about+my+hobbies"

# Ask about coding preferences  
curl "http://localhost:8080/query?q=What+are+my+coding+preferences"
```

### Manual Testing
```bash
# POST request
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are my favorite footballers?"}'

# GET request
curl "http://localhost:8080/query?q=What+do+you+know+about+motorcycles"
```

## 📋 Prerequisites

1. **Graphiti MCP Server running** on `http://127.0.0.1:8000/sse`
2. **Python 3.10+** (for MCP compatibility)
3. **Environment file** (`.env`) with your API keys
4. **Docker** (optional, for containerized deployment)

## 🔧 Configuration

The API uses these environment variables:
- `PORT=8080` - API server port
- `HOST=0.0.0.0` - API server host  
- `DEBUG=false` - Enable Flask debug mode

## 📝 Example Response

```json
{
  "query": "What do you know about the user?",
  "response": "I know that you are interested in football players Pirlo and Zidane, love two-stroke Italian motorcycles, train in Muay Thai for 8 years, enjoy whisky and soda, and have plans to buy a vineyard when you are rich.",
  "status": "success"
}
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Make sure Graphiti MCP server is running on port 8000 |
| "No response received" | Check if your knowledge graph has data |
| Authentication errors | Verify your `.env` file has correct API keys |
| Import errors | Make sure you're using Python 3.10+ |

## 🏗️ Architecture

```
Claude Code → curl → Flask API → MCP Agent → Graphiti Server → Neo4j
```

## 📚 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API documentation |
| `/health` | GET | Health check |
| `/query` | POST | Query with JSON: `{"query": "your question"}` |
| `/query?q=<query>` | GET | Query with URL parameter |

## 🎯 Claude Code Integration

Add this to your Claude Code workflow:

```bash
# Get context about the user before summarizing work
CONTEXT=$(curl -s "http://localhost:8080/query?q=What+do+you+know+about+the+user")
echo "User context: $CONTEXT"
```

Now Claude Code can use your personal knowledge graph for better, more personalized responses! 🎉