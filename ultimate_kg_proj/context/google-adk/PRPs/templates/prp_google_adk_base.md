---
name: "Google ADK Agent Development PRP"
description: "Template optimized for AI agents to build sophisticated agent systems using Google's Agent Development Kit with multi-agent coordination and Google Cloud integration"
---

## Purpose

Agent optimized for building **[AGENT_SYSTEM_NAME]** using Google's Agent Development Kit with multi-agent coordination, tool integration, and Google Cloud deployment capabilities.

## Core Principles

1. **Agent-First Architecture**: Design sophisticated AI agents as the primary development paradigm
2. **Multi-Agent Coordination**: Implement complex agent orchestration and delegation patterns
3. **Google Cloud Native**: Deep integration with Vertex AI, Cloud Run, and Google Cloud services
4. **Tool-Rich Environment**: Comprehensive integration of built-in and custom tools
5. **Production Ready**: Include deployment, monitoring, and cost optimization for enterprise use

---

## Goal

Build a comprehensive agent system for **[AGENT_SYSTEM_PURPOSE]** that includes:

- Individual specialized agents with clear responsibilities
- Multi-agent coordinator with proper delegation patterns
- Custom tool integration with comprehensive error handling
- Google Cloud deployment with Vertex AI and Cloud Run
- Production monitoring and cost optimization strategies

## Why

- **Agent Sophistication**: Create intelligent agents that can handle complex, multi-step tasks
- **Scalable Architecture**: Multi-agent systems that scale with problem complexity
- **Google Cloud Integration**: Leverage Google's AI and cloud infrastructure
- **Production Ready**: Enterprise-grade deployment and monitoring capabilities
- **Cost Effective**: Optimized resource usage and cost management

## What

### Agent System Components

**Individual Agents:**
- **Primary Coordinator**: Main agent that delegates tasks to specialized agents
- **Search Agent**: Handles web search and information gathering tasks
- **Task Agent**: Executes specific business logic and data processing
- **Integration Agent**: Manages external API calls and service integrations

**Multi-Agent Coordination:**
- Hierarchical delegation with clear agent responsibilities
- Dynamic routing based on task requirements
- State management across agent interactions
- Error handling and retry mechanisms

**Tool Integration:**
- Built-in Google ADK tools (google_search, code_execution)
- Custom tools for domain-specific operations
- Tool orchestration and chaining patterns
- Comprehensive tool error handling

**Google Cloud Integration:**
- Vertex AI model integration for LLM access
- Cloud Run deployment for scalable agent hosting
- Service account authentication and IAM configuration
- Cost monitoring and optimization strategies

### Success Criteria

- [ ] Multi-agent system with proper coordination and delegation
- [ ] Individual agents with clear, focused responsibilities
- [ ] Custom and built-in tool integration working correctly
- [ ] Google Cloud authentication and deployment configured
- [ ] Agent system handles errors gracefully with retry mechanisms
- [ ] Production monitoring and logging implemented
- [ ] Cost optimization strategies in place
- [ ] Comprehensive testing for agent behavior and coordination
- [ ] Documentation complete with deployment instructions

## All Needed Context

### Documentation & References (RESEARCH REQUIRED)

```yaml
# GOOGLE ADK FOUNDATION - Core framework understanding
- url: https://google.github.io/adk-docs/
  why: Official Google ADK documentation with agent architecture and API reference

- url: https://google.github.io/adk-docs/get-started/quickstart/
  why: Getting started guide with agent creation and multi-agent patterns

- url: https://github.com/google/adk-python
  why: Main Python repository with source code and implementation examples

- url: https://github.com/google/adk-samples/tree/main/python
  why: Ready-to-use sample agents demonstrating various ADK patterns

# GOOGLE CLOUD INTEGRATION - Deployment and scaling
- url: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart
  why: Google Cloud quickstart for ADK with Vertex AI integration

- url: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/develop/adk
  why: Vertex AI Agent Engine development patterns

- url: https://cloud.google.com/run/docs
  why: Cloud Run deployment for containerized agent applications

# AGENT DEVELOPMENT PATTERNS - Implementation guides
- url: https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/
  why: Official Google blog with multi-agent application patterns

- url: https://www.datacamp.com/tutorial/agent-development-kit-adk
  why: Comprehensive ADK tutorial with practical examples

# CONTEXT ENGINEERING FOUNDATION - Base framework
- file: ../../CLAUDE.md
  why: Google ADK global rules and development standards

- file: ../../../README.md
  why: Core context engineering principles adapted for agent development
```

### Google ADK Architecture Patterns

```python
# Agent Creation Patterns (to implement)
class AgentSystemArchitecture:
    # Individual Agent Types
    agent_types = {
        "LlmAgent": "Core agent with LLM integration and instructions",
        "Agent": "Simplified agent interface for basic use cases",
        "BaseAgent": "Custom agent base class for specialized implementations"
    }
    
    # Multi-Agent Coordination
    coordination_patterns = {
        "hierarchical": "Parent coordinator with specialized sub-agents",
        "sequential": "Step-by-step agent workflow execution",
        "parallel": "Concurrent agent processing",
        "dynamic": "LLM-driven agent selection and routing"
    }
    
    # Tool Integration
    tool_patterns = {
        "built_in": ["google_search", "code_execution"],
        "custom": "@tool decorator for domain-specific functions",
        "orchestration": "Multi-tool coordination within agents",
        "error_handling": "Retry and fallback mechanisms"
    }
    
    # Google Cloud Integration
    cloud_patterns = {
        "vertex_ai": "Model hosting and management",
        "cloud_run": "Scalable agent deployment",
        "authentication": "Service account and IAM setup",
        "monitoring": "Logging and cost tracking"
    }
```

### Implementation Requirements

```typescript
// CRITICAL: Agent system must follow these patterns

// 1. Agent Specialization
const agent_design = {
  single_responsibility: "Each agent has one clear purpose",
  clear_instructions: "Specific, actionable instructions for each agent",
  tool_integration: "Appropriate tools assigned to each agent",
  error_handling: "Graceful failure and retry mechanisms"
};

// 2. Multi-Agent Coordination
const coordination_design = {
  hierarchy: "Clear parent-child relationships",
  delegation: "Proper task routing to appropriate agents",
  communication: "State sharing between agents",
  conflict_resolution: "Handling competing agent responses"
};

// 3. Google Cloud Integration
const cloud_integration = {
  authentication: "Service account setup and IAM policies",
  deployment: "Container and serverless deployment options",
  scaling: "Auto-scaling based on demand",
  cost_optimization: "Resource limits and usage monitoring"
};

// 4. Production Readiness
const production_patterns = {
  monitoring: "Comprehensive logging and metrics",
  error_tracking: "Agent failure detection and alerting",
  cost_control: "Budget limits and usage optimization",
  security: "Input validation and access control"
};
```

## Implementation Blueprint

### Agent System Development

```yaml
Development Task 1 - Agent Architecture Design:
  DESIGN complete agent system architecture:
    - Identify individual agent responsibilities and capabilities
    - Plan multi-agent coordination and delegation patterns
    - Design tool integration strategy for each agent
    - Plan Google Cloud integration and deployment strategy

Development Task 2 - Individual Agent Implementation:
  IMPLEMENT specialized agents:
    - Create primary coordinator agent with delegation logic
    - Implement search agent with google_search tool integration
    - Build task-specific agents for domain operations
    - Configure each agent with appropriate models and instructions

Development Task 3 - Multi-Agent Coordination:
  IMPLEMENT agent coordination patterns:
    - Set up hierarchical agent relationships using sub_agents
    - Implement dynamic routing and task delegation
    - Create state management across agent interactions
    - Add error handling and retry mechanisms

Development Task 4 - Tool Integration:
  IMPLEMENT comprehensive tool ecosystem:
    - Integrate built-in Google ADK tools (search, code execution)
    - Create custom tools using @tool decorator
    - Implement tool orchestration and chaining
    - Add comprehensive error handling for tool failures

Development Task 5 - Google Cloud Integration:
  CONFIGURE Google Cloud deployment:
    - Set up service account authentication
    - Configure Vertex AI model access and quotas
    - Create Cloud Run deployment configuration
    - Implement cost monitoring and optimization

Development Task 6 - Testing and Validation:
  IMPLEMENT comprehensive testing:
    - Create agent behavior tests with mock responses
    - Test multi-agent coordination and communication
    - Validate tool integration and error handling
    - Test Google Cloud deployment and authentication

Development Task 7 - Production Deployment:
  DEPLOY agent system to Google Cloud:
    - Container deployment to Cloud Run
    - Environment configuration and secrets management
    - Monitoring and logging setup
    - Cost optimization and resource limits
```

### Google Cloud Configuration

```yaml
AUTHENTICATION_SETUP:
  service_account:
    - Create dedicated service account for agent system
    - Configure IAM roles: Vertex AI User, Cloud Run Developer
    - Download service account key for local development
    - Set GOOGLE_APPLICATION_CREDENTIALS environment variable

VERTEX_AI_CONFIGURATION:
  model_access:
    - Enable Vertex AI API in Google Cloud project
    - Configure regional model availability (us-central1 recommended)
    - Set up model quotas and usage limits
    - Configure billing and cost monitoring

CLOUD_RUN_DEPLOYMENT:
  container_setup:
    - Create Dockerfile for agent application
    - Configure Cloud Run service with appropriate resources
    - Set up environment variables and secrets
    - Configure auto-scaling and request timeout
```

### Agent Development Standards

```python
# Standard ADK Agent Implementation Pattern
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search, tool
from dotenv import load_dotenv
import os

# Load environment configuration
load_dotenv()

# Custom tool example
@tool
def domain_specific_operation(parameter: str) -> str:
    """Perform domain-specific operation with proper error handling."""
    try:
        # Implementation here
        return f"Operation result for {parameter}"
    except Exception as e:
        return f"Operation failed: {str(e)}"

# Individual specialized agent
search_agent = Agent(
    name="search_specialist",
    model=os.getenv("ADK_MODEL", "gemini-2.0-flash"),
    instruction="You are a search specialist. Use Google Search to find comprehensive information.",
    description="Specialized agent for web search and information gathering",
    tools=[google_search]
)

# Task-specific agent
task_agent = LlmAgent(
    name="task_executor",
    model=os.getenv("ADK_MODEL", "gemini-2.0-flash"),
    instruction="You execute specific tasks using available tools.",
    tools=[domain_specific_operation]
)

# Multi-agent coordinator
coordinator = LlmAgent(
    name="system_coordinator",
    model=os.getenv("ADK_MODEL", "gemini-2.0-flash"),
    instruction="You coordinate between search and task agents to complete complex objectives.",
    description="Main coordinator that delegates tasks to specialized agents",
    sub_agents=[search_agent, task_agent]
)
```

## Validation Loop

### Level 1: Agent System Structure Validation

```bash
# CRITICAL: Verify complete agent system structure
find . -name "*.py" -type f | sort
ls -la agents/ tools/ configs/ deployments/

# Verify Python syntax and imports
python -m py_compile agents/*.py tools/*.py configs/*.py
python -c "from google.adk.agents import Agent, LlmAgent; print('ADK imports successful')"

# Expected: All agent files present and syntactically correct
# If failing: Fix Python syntax and ADK import issues
```

### Level 2: Agent Functionality Validation

```bash
# Test individual agent creation
python -c "
from agents.main_agent import create_coordinator_agent
agent = create_coordinator_agent()
print(f'Coordinator created: {agent.name}')
print(f'Sub-agents: {len(agent.sub_agents)}')
"

# Test tool integration
python -c "
from tools.custom_tools import *
print('Custom tools imported successfully')
"

# Expected: Agents create successfully with proper coordination
# If failing: Debug agent creation and tool integration issues
```

### Level 3: Google Cloud Integration Validation

```bash
# Test Google Cloud authentication
gcloud auth application-default print-access-token > /dev/null 2>&1 && echo "GCloud auth configured" || echo "GCloud auth needs setup"

# Test environment configuration
python -c "
from configs.environment import get_google_cloud_config
config = get_google_cloud_config()
print(f'Project: {config.get(\"project_id\", \"Not configured\")}')
"

# Test deployment configuration
test -f deployments/Dockerfile && echo "Docker config present"
test -f deployments/cloud_run.yaml && echo "Cloud Run config present"

# Expected: Google Cloud integration properly configured
# If failing: Configure authentication and deployment settings
```

### Level 4: Production Readiness Validation

```bash
# Test agent system with mock interactions
python -m pytest tests/ -v

# Validate deployment configuration
docker build -t test-agent-system . && echo "Docker build successful"

# Test cost optimization settings
python -c "
from configs.deployment_config import get_resource_limits
limits = get_resource_limits()
print(f'Resource limits configured: {limits}')
"

# Expected: All tests pass and deployment ready
# If failing: Fix test failures and deployment configuration
```

## Final Validation Checklist

### Agent System Completeness

- [ ] Multi-agent coordinator with proper sub-agent delegation: `grep -r "sub_agents" agents/`
- [ ] Individual specialized agents with clear responsibilities: `ls agents/specialized_agents/`
- [ ] Custom and built-in tool integration: `grep -r "@tool\|google_search" tools/`
- [ ] Google Cloud authentication configured: `test -f .env.example`
- [ ] Deployment configuration present: `ls deployments/`

### Quality and Production Readiness

- [ ] No syntax errors: `python -m py_compile **/*.py`
- [ ] ADK patterns properly implemented: `grep -r "LlmAgent\|Agent" agents/`
- [ ] Error handling comprehensive: `grep -r "try:\|except:" agents/ tools/`
- [ ] Testing framework complete: `ls tests/`
- [ ] Documentation comprehensive: `test -f README.md`

### Google Cloud Integration

- [ ] Service account configuration: `grep -r "GOOGLE_APPLICATION_CREDENTIALS"`
- [ ] Vertex AI integration: `grep -r "vertex-ai\|gemini" configs/`
- [ ] Cloud Run deployment: `test -f deployments/cloud_run.yaml`
- [ ] Cost monitoring: `grep -r "cost\|limit" configs/`
- [ ] Production monitoring: `grep -r "logging\|monitoring" configs/`

---

## Anti-Patterns to Avoid

### Agent Development

- ❌ Don't create overly complex agent hierarchies - keep coordination patterns simple
- ❌ Don't skip tool error handling - implement comprehensive retry mechanisms
- ❌ Don't ignore Google Cloud authentication - proper service account setup is critical
- ❌ Don't hardcode configurations - use environment variables for all settings

### Multi-Agent Coordination

- ❌ Don't create circular dependencies between agents - maintain clear hierarchy
- ❌ Don't skip state management - agents need to share context appropriately
- ❌ Don't ignore agent coordination failures - implement proper fallback mechanisms
- ❌ Don't over-complicate delegation - each agent should have clear responsibilities

### Google Cloud Integration

- ❌ Don't skip cost monitoring - model usage can accumulate quickly
- ❌ Don't ignore regional limitations - models have different availability by region
- ❌ Don't skip security configuration - implement proper IAM and access controls
- ❌ Don't forget monitoring - comprehensive logging is essential for production