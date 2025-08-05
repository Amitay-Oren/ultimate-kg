# Google Agent Development Kit (ADK) - Global Rules for AI Agent Development

This file contains the global rules and principles that apply to ALL Google Agent Development Kit (ADK) development work. These rules are specialized for building production-grade AI agents, multi-agent systems, and complex agentic workflows using Google's ADK framework.

## 🔄 Google ADK Core Principles

**IMPORTANT: These principles apply to ALL Google ADK agent development:**

### Agent Development Workflow
- **Always start with INITIAL.md** - Define agent requirements before generating PRPs
- **Use the PRP pattern**: INITIAL.md → `/generate-google-adk-prp INITIAL.md` → `/execute-google-adk-prp PRPs/filename.md`
- **Follow validation loops** - Each PRP must include agent testing with mock and real LLM validation
- **Context is King** - Include ALL necessary ADK patterns, examples, and Google Cloud integration

### Research Methodology for AI Agents
- **Web search extensively** - Always research Google ADK patterns and best practices
- **Study official documentation** - google.github.io/adk-docs is the authoritative source
- **Pattern extraction** - Identify reusable agent architectures and multi-agent coordination patterns
- **Gotcha documentation** - Document Google Cloud integration issues, agent coordination complexities

## 📚 Project Awareness & Context

- **Use Poetry for dependency management** and virtual environments for all ADK projects
- **Use consistent Google ADK naming conventions** and agent structure patterns
- **Follow established agent directory organization** patterns (agents/, tools/, configs/)
- **Leverage Google ADK examples extensively** - Study existing patterns before creating new agents

## 🧱 Agent Structure & Modularity

- **Never create files longer than 500 lines** - Split into modules when approaching limit
- **Organize agent code into clearly separated modules** grouped by responsibility:
  - `agents/` - Agent definitions and coordination logic
  - `tools/` - Custom tool functions used by agents
  - `configs/` - Agent configurations and environment setup
  - `deployments/` - Cloud Run and Vertex AI deployment configurations
- **Use clear, consistent imports** - Import from google.adk package appropriately
- **Use python-dotenv and .env files** for environment variables and Google Cloud configuration
- **Never hardcode sensitive information** - Always use environment variables for API keys and credentials

## 🤖 Google ADK Development Standards

### Agent Creation Patterns
- **Use model-agnostic design** - Support Gemini, GPT-4o, Claude, Mistral via LiteLLM
- **Implement multi-agent coordination** - Use sub_agents for hierarchical delegation
- **Define clear agent instructions** - Use specific, task-focused instructions for each agent
- **Include comprehensive tool integration** - Both built-in and custom tools

### Tool Integration Standards
- **Use @tool decorator** for custom tool creation with proper typing
- **Use built-in tools** - google_search, code_execution for common operations
- **Implement proper parameter validation** - Use type hints and docstrings for all tools
- **Handle tool errors gracefully** - Implement retry mechanisms and error recovery

### Environment Variable Configuration with python-dotenv
```python
# Use python-dotenv for proper Google Cloud configuration management
from dotenv import load_dotenv
import os
from google.adk.agents import Agent, LlmAgent

# Load environment variables from .env file
load_dotenv()

def get_agent_config():
    """Get agent configuration from environment variables."""
    return {
        "model": os.getenv("ADK_MODEL", "gemini-2.0-flash"),
        "google_cloud_project": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "vertex_ai_location": os.getenv("VERTEX_AI_LOCATION", "us-central1"),
        "service_account_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    }

# Create agent with environment-based configuration
agent = Agent(
    name="my_agent",
    model=get_agent_config()["model"],
    instruction="You are a helpful AI assistant."
)
```

### Multi-Agent Coordination Standards
- **Use hierarchical patterns** - Parent coordinator with specialized sub-agents
- **Implement clear delegation** - Each sub-agent has specific responsibilities
- **Design for scalability** - Agent coordination patterns that scale with complexity
- **Test agent interactions** - Validate multi-agent communication and coordination

## ✅ Task Management for AI Development

- **Break agent development into clear steps** with specific completion criteria
- **Mark tasks complete immediately** after finishing agent implementations
- **Update task status in real-time** as agent development progresses
- **Test agent behavior** before marking implementation tasks complete

## 📎 Google ADK Coding Standards

### Agent Architecture
```python
# Follow Google ADK patterns - clear agent specialization
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search, tool
from dotenv import load_dotenv
import os

# Load environment configuration
load_dotenv()

# Create specialized agents
@tool
def custom_calculation(x: float, y: float) -> float:
    """Perform custom calculation."""
    return x * y + 10

# Simple agent with tools
search_agent = Agent(
    name="search_assistant",
    model="gemini-2.0-flash",
    instruction="You are a search assistant. Use Google Search to find information.",
    description="An assistant that can search the web.",
    tools=[google_search]
)

# Multi-agent coordinator
calculator_agent = LlmAgent(
    name="calculator",
    model="gemini-2.0-flash",
    instruction="You perform calculations using available tools.",
    tools=[custom_calculation]
)

coordinator = LlmAgent(
    name="coordinator",
    model="gemini-2.0-flash",
    instruction="You coordinate between search and calculation agents.",
    description="Coordinates search and calculation tasks.",
    sub_agents=[search_agent, calculator_agent]
)
```

### Google Cloud Integration Best Practices
- **Service account authentication** - Use service accounts for production deployments
- **Environment-based configuration** - Different configs for dev/staging/production
- **IAM role management** - Proper permissions for Vertex AI and other Google Cloud services
- **Cost monitoring** - Track model usage and implement cost controls
- **Regional deployment** - Use appropriate regions for model availability and latency

### Common Google ADK Gotchas
- **Model availability issues** - Different models available in different regions
- **Agent coordination complexity** - Over-complex multi-agent hierarchies can be difficult to debug
- **Tool execution timeouts** - Long-running tools may timeout in agent workflows
- **Google Cloud authentication failures** - Service account setup and permissions issues
- **Cost accumulation** - Model usage costs can accumulate quickly without monitoring

## 🔍 Research Standards for AI Agents

- **Use web search extensively** - Leverage available web search capabilities for ADK research
- **Study official Google ADK documentation** - google.github.io/adk-docs has comprehensive guides
- **Research Google Cloud integration patterns** - Understand Vertex AI and Cloud Run deployment options
- **Document integration patterns** - Include Google Cloud service integration examples

## 🎯 Implementation Standards for AI Agents

- **Follow the PRP workflow religiously** - Don't skip agent validation steps
- **Always test agents thoroughly** - Validate agent logic with both mock and real responses
- **Use existing ADK patterns** rather than creating from scratch
- **Include comprehensive error handling** for agent failures and tool errors
- **Test multi-agent coordination** when implementing complex agent systems

## 🚫 Anti-Patterns to Always Avoid

- ❌ Don't skip agent testing - Always validate agent behavior before deployment
- ❌ Don't hardcode model strings - Use environment-based configuration
- ❌ Don't ignore Google Cloud authentication - Proper service account setup is critical
- ❌ Don't create overly complex agent hierarchies - Keep coordination patterns simple and testable
- ❌ Don't ignore cost implications - Monitor model usage and implement cost controls
- ❌ Don't forget tool error handling - Implement proper retry and graceful degradation
- ❌ Don't skip Google Cloud integration - ADK is designed for Google Cloud deployment

## 🔧 Tool Usage Standards for AI Development

- **Use web search extensively** for Google ADK research and documentation
- **Follow Google ADK command patterns** for slash commands and agent workflows
- **Use agent validation loops** to ensure quality at each development step
- **Test with multiple model providers** to ensure agent compatibility

## 🧪 Testing & Reliability for AI Agents

- **Always create comprehensive agent tests** for tools, coordination, and error handling
- **Test agent behavior with mock responses** before using real model providers
- **Include edge case testing** for agent failures and tool provider issues
- **Test multi-agent coordination** to ensure proper delegation and communication
- **Validate Google Cloud integration** works correctly in test environments

## 🌊 Google Cloud Deployment Standards

### Cloud Run Deployment
- **Use Docker containerization** for consistent deployment environments
- **Implement proper health checks** for agent service availability
- **Configure auto-scaling** based on agent request patterns
- **Set appropriate resource limits** for memory and CPU usage
- **Use environment variables** for configuration management

### Vertex AI Agent Engine Integration
- **Configure proper IAM roles** for Vertex AI access
- **Use regional endpoints** for optimal performance
- **Implement proper logging** for agent operations and debugging
- **Set up monitoring** for agent performance and cost tracking
- **Configure model quotas** to prevent cost overruns

### Authentication and Security
- **Use service accounts** for production agent deployments
- **Implement proper IAM policies** with least privilege principles
- **Secure API endpoints** with proper authentication and authorization
- **Audit agent operations** for security and compliance
- **Implement input validation** to prevent prompt injection attacks

These global rules apply specifically to Google ADK agent development and ensure production-ready AI applications with proper multi-agent coordination, Google Cloud integration, and comprehensive testing practices.