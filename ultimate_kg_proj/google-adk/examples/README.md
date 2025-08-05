# Google ADK Agent Examples

This directory contains real-world Google Agent Development Kit (ADK) examples copied from production implementations. These examples demonstrate various agent patterns and multi-agent coordination strategies.

## Available Examples

### 1. KG Broker Agent (`kg_broker_agent/`)
**Source**: cc-a2a-agents project
**Purpose**: Fact-ingestion agent that stores summaries in a Graphiti knowledge graph
**Key Features**:
- MCP (Model Context Protocol) toolset integration
- Graphiti knowledge graph storage
- Asynchronous agent execution
- Memory storage with timestamps

**Files**:
- `agent.py` - Main agent implementation with MCP integration
- `prompt.py` - Specialized prompt for fact ingestion
- `run_agent.py` - Agent execution script

### 2. Parallel Extraction System (`parallel_extraction_system/`)
**Source**: medium_adk-kg project
**Purpose**: Multi-agent system for concurrent fact and gap extraction
**Key Features**:
- Sequential and Parallel agent coordination
- Fact extraction and knowledge gap identification
- Agent tool integration for complex workflows
- Structured output schemas

**Files**:
- `agent.py` - Multi-agent coordination with parallel processing
- `schemas.py` - Pydantic schemas for structured outputs

### 3. Orchestrator Agent (`orchestrator_agent/`)
**Source**: medium_adk-kg project
**Purpose**: Advanced user-facing agent that coordinates with specialized sub-agents
**Key Features**:
- User interaction and conversation handling
- Task delegation to specialized agents
- Integration with processing workflows

**Files**:
- `agent.py` - Main orchestrator implementation
- `prompt.py` - Orchestrator agent instructions
- `job.txt` - Example job description

### 4. MLE Pipeline System (`mle_pipeline_system/`)
**Source**: mle-star project
**Purpose**: Machine Learning Engineering pipeline with sequential agent workflows
**Key Features**:
- Sequential agent workflows for ML tasks
- Callback functions for state management
- Sub-agent specialization (initialization, refinement, ensemble, submission)
- Workspace management and file operations

**Files**:
- `agent.py` - Main pipeline coordinator
- `prompt.py` - System instructions
- `sub_agents/` - Specialized agents for different ML tasks
- `shared_libraries/` - Common utilities and tools

## Usage Patterns Demonstrated

### MCP Integration
```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams

toolset = MCPToolset(
    connection_params=SseConnectionParams(url="http://127.0.0.1:8000/sse")
)
```

### Multi-Agent Coordination
```python
from google.adk.agents import SequentialAgent, ParallelAgent

# Sequential processing
sequential_workflow = SequentialAgent(
    name="fact_handling",
    sub_agents=[extractor, processor]
)

# Parallel processing
parallel_workflow = ParallelAgent(
    name="concurrent_processing", 
    sub_agents=[fact_workflow, gaps_workflow]
)
```

### Agent Tool Integration
```python
from google.adk.tools.agent_tool import AgentTool

processing_tool = AgentTool(agent=processing_agent)
```

### State Management
```python
def save_state(callback_context):
    workspace_dir = callback_context.state.get("workspace_dir", "")
    # Save state logic
    return None
```

## Running the Examples

Each example directory contains its own README and setup instructions. Generally:

1. **Set up environment**:
   ```bash
   pip install google-adk
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the agent**:
   ```bash
   python agent.py
   # or 
   python run_agent.py
   ```

## Key Learning Points

- **Agent Specialization**: Each agent has a clear, focused purpose
- **Tool Integration**: Seamless integration with MCP tools and custom functions
- **Multi-Agent Patterns**: Sequential, parallel, and hierarchical coordination
- **State Management**: Proper handling of agent state and context
- **Error Handling**: Robust error handling and cleanup procedures
- **Production Patterns**: Real-world implementation patterns and best practices

These examples provide excellent starting points for building your own Google ADK agent systems.