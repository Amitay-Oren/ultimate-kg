---
name: "Google Agent Development Kit (ADK) Context Engineering Template PRP"
description: "Complete template package for building AI agents and multi-agent systems using Google's Agent Development Kit with comprehensive Google Cloud integration"
---

## Purpose

Generate a complete context engineering template package for **Google Agent Development Kit (ADK)** that enables developers to rapidly build intelligent AI agents, multi-agent systems, and complex agentic workflows with proper Google Cloud integration, deployment patterns, and production-ready development practices.

## Core Principles

1. **Agent-First Development**: Emphasize building sophisticated AI agents as the primary development paradigm
2. **Multi-Agent Architecture**: Support complex agent orchestration and coordination patterns
3. **Google Cloud Native**: Deep integration with Vertex AI, Cloud Run, and Google Cloud services
4. **Model Agnostic**: Support for multiple LLM providers while optimizing for Google's Gemini models
5. **Production Ready**: Include deployment, monitoring, and scaling patterns for enterprise use

---

## Goal

Create a comprehensive context engineering template package for **Google Agent Development Kit (ADK)** that includes:

- Domain-specific CLAUDE.md implementation guide with ADK patterns
- Specialized PRP generation and execution commands for agent development
- Google ADK-specific base PRP template with agent architecture patterns
- Complete working examples from basic agents to complex multi-agent systems
- Google Cloud deployment and integration documentation
- Comprehensive validation loops for agent development and testing

## Why

- **Accelerate Agent Development**: Enable rapid creation of sophisticated AI agents using Google's framework
- **Multi-Agent Mastery**: Provide proven patterns for complex agent orchestration and coordination
- **Google Cloud Integration**: Streamline deployment and scaling on Google Cloud Platform
- **Production Readiness**: Include enterprise-grade patterns for monitoring, security, and cost optimization
- **Framework Adoption**: Lower barriers to adopting Google's Agent Development Kit

## What

### Template Package Components

**Complete Directory Structure:**
```
use-cases/google-adk/
├── CLAUDE.md                           # Google ADK implementation guide
├── .claude/commands/
│   ├── generate-google-adk-prp.md      # ADK-specific PRP generation
│   └── execute-google-adk-prp.md       # ADK-specific PRP execution  
├── PRPs/
│   ├── templates/
│   │   └── prp_google_adk_base.md      # ADK-specific base PRP template
│   ├── ai_docs/                        # ADK documentation and patterns
│   │   ├── adk_architecture_patterns.md
│   │   ├── multi_agent_coordination.md
│   │   └── google_cloud_integration.md
│   └── INITIAL.md                      # Example agent feature request
├── examples/                           # Comprehensive ADK examples
│   ├── basic_chat_agent/               # Simple conversational agent
│   ├── search_assistant_agent/         # Tool-enabled agent with search
│   ├── multi_agent_system/             # Complex agent coordination
│   ├── workflow_agents/                # Sequential/parallel workflows
│   ├── cloud_run_deployment/           # Cloud Run deployment example
│   └── vertex_ai_integration/          # Vertex AI Agent Engine example
├── copy_template.py                    # Template deployment script
└── README.md                           # Comprehensive usage guide
```

**Google ADK Integration:**
- Agent architecture patterns and best practices
- Multi-agent system design and coordination
- Google Cloud service integration (Vertex AI, Cloud Run, Cloud Storage)
- Tool creation and integration patterns
- Agent evaluation and testing frameworks
- Production deployment and monitoring

**Context Engineering Adaptation:**
- ADK-specific research processes and documentation patterns
- Agent development workflow optimization
- Google Cloud-appropriate validation loops
- Multi-agent system testing and integration patterns

### Success Criteria

- [ ] Complete Google ADK template package structure generated
- [ ] All required files present with ADK-specific content
- [ ] Agent development patterns accurately represent ADK best practices
- [ ] Multi-agent coordination patterns properly documented
- [ ] Google Cloud integration patterns included and tested
- [ ] Validation loops appropriate for agent development and testing
- [ ] Template immediately usable for creating ADK-based agent projects
- [ ] Comprehensive examples from basic to complex agent systems
- [ ] Production deployment patterns included and validated

## All Needed Context

### Documentation & References (RESEARCHED FROM WEB)

```yaml
# GOOGLE ADK FOUNDATION - Core framework understanding
- url: https://google.github.io/adk-docs/
  why: Official Google ADK documentation with architecture, concepts, and API reference

- url: https://google.github.io/adk-docs/get-started/quickstart/
  why: Getting started guide with setup, installation, and first agent creation

- url: https://github.com/google/adk-python
  why: Main Python repository with source code, examples, and development patterns

- url: https://github.com/google/adk-samples/tree/main/python
  why: Ready-to-use sample agents demonstrating various ADK implementation patterns

- url: https://github.com/google/adk-docs
  why: Documentation repository with additional examples and detailed guides

# GOOGLE CLOUD INTEGRATION - Deployment and scaling patterns
- url: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart
  why: Google Cloud quickstart for ADK with Vertex AI integration

- url: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/develop/adk
  why: Vertex AI Agent Engine development with ADK patterns

- url: https://cloud.google.com/run/docs
  why: Cloud Run deployment patterns for containerized agent applications

- url: https://cloud.google.com/vertex-ai/docs
  why: Vertex AI documentation for model integration and management

# LEARNING RESOURCES - Comprehensive guides and tutorials
- url: https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/
  why: Official Google Developers Blog post introducing ADK concepts and use cases

- url: https://www.datacamp.com/tutorial/agent-development-kit-adk
  why: Comprehensive tutorial on Google's Agent Development Kit with practical examples

- url: https://www.siddharthbharath.com/the-complete-guide-to-googles-agent-development-kit-adk/
  why: Complete guide to Google's ADK with detailed explanations and code examples

# CONTEXT ENGINEERING FOUNDATION - Base framework to extend
- file: ../../../README.md
  why: Core context engineering principles and workflow to adapt

- file: ../../../.claude/commands/generate-prp.md
  why: Base PRP generation patterns to specialize for ADK development

- file: ../../../PRPs/templates/prp_base.md
  why: Base PRP template structure to specialize for agent development

# REFERENCE IMPLEMENTATIONS - Proven specialization patterns
- file: ../pydantic-ai/CLAUDE.md
  why: Example of AI agent framework specialization patterns

- file: ../mcp-server/CLAUDE.md
  why: Example of technology-specific implementation guide patterns
```

### Google ADK Architecture Analysis (FROM WEB RESEARCH)

```python
# Core ADK Components and Patterns (researched from documentation)
class ADKArchitecture:
    # Agent Types and Creation Patterns
    agent_types = {
        "LlmAgent": "Core agent type with LLM integration",
        "BaseAgent": "Base class for custom agent implementations", 
        "Agent": "Simplified agent creation interface"
    }
    
    # Multi-Agent Patterns
    coordination_patterns = {
        "hierarchical": "Parent-child agent relationships via sub_agents",
        "sequential": "Step-by-step agent workflow execution",
        "parallel": "Concurrent agent execution patterns",
        "dynamic_routing": "LLM-driven agent selection and delegation"
    }
    
    # Tool Integration
    tool_patterns = {
        "built_in_tools": ["google_search", "code_execution"],
        "custom_tools": "Function-based tool creation patterns",
        "tool_registration": "Agent tool assignment and management",
        "tool_orchestration": "Multi-tool coordination within agents"
    }
    
    # Model Integration
    model_support = {
        "gemini": "Primary Google model integration (gemini-2.0-flash)",
        "multi_provider": "OpenAI, Anthropic, Mistral via LiteLLM",
        "model_agnostic": "Framework-independent model selection"
    }
    
    # Deployment Patterns
    deployment_options = {
        "local_development": "Local testing with developer UI",
        "cloud_run": "Containerized deployment on Google Cloud",
        "vertex_ai": "Vertex AI Agent Engine integration",
        "custom_deployment": "Flexible deployment configuration"
    }
```

### Google Cloud Integration Patterns (FROM RESEARCH)

```yaml
GOOGLE_CLOUD_SERVICES:
  vertex_ai:
    - Model hosting and management
    - Agent Engine for production deployment
    - Vector Search for agent memory
    - AI Platform Pipelines for agent workflows
  
  cloud_run:
    - Serverless agent deployment
    - Auto-scaling agent instances
    - Container-based agent packaging
    - HTTP/gRPC agent endpoints
  
  cloud_storage:
    - Agent state persistence
    - Training data management
    - Model artifact storage
    - Log and metric storage
  
  cloud_functions:
    - Event-driven agent triggers
    - Lightweight agent operations
    - Integration with other Google services
    - Cost-effective simple agent deployment

AUTHENTICATION_PATTERNS:
  service_accounts:
    - Agent service identity
    - Google Cloud API access
    - Fine-grained permissions
    - Secure credential management
  
  iam_roles:
    - Agent permission management
    - Resource access control
    - Multi-tenant agent security
    - Audit and compliance
```

### ADK Development Patterns (FROM EXAMPLES AND DOCUMENTATION)

```python
# Agent Creation Patterns (from ADK samples)
basic_agent_pattern = """
from google.adk.agents import Agent
from google.adk.tools import google_search

# Simple agent with built-in tools
agent = Agent(
    name="search_assistant",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant. Answer questions using search.",
    description="An assistant that can search the web.",
    tools=[google_search]
)
"""

multi_agent_pattern = """
from google.adk.agents import LlmAgent

# Define specialized agents
greeter = LlmAgent(
    name="greeter",
    model="gemini-2.0-flash",
    instruction="Greet users warmly and professionally."
)

task_executor = LlmAgent(
    name="task_executor", 
    model="gemini-2.0-flash",
    instruction="Execute specific tasks assigned by coordinator."
)

# Create coordinator agent
coordinator = LlmAgent(
    name="coordinator",
    model="gemini-2.0-flash",
    description="I coordinate greetings and task execution.",
    sub_agents=[greeter, task_executor]
)
"""

# Tool Creation Patterns
custom_tool_pattern = """
from google.adk.tools import tool

@tool
def currency_exchange(from_currency: str, to_currency: str) -> str:
    \"\"\"Get exchange rate between currencies.\"\"\"
    # Implementation here
    return f"Exchange rate from {from_currency} to {to_currency}"

# Add to agent
agent = Agent(
    name="finance_assistant",
    tools=[currency_exchange]
)
"""
```

### Known ADK Development Patterns (FROM RESEARCH)

```typescript
// CRITICAL: ADK development must follow these patterns

// 1. Agent-First Architecture
const agent_patterns = {
  single_agent: "LlmAgent with specific instruction and tools",
  multi_agent: "Coordinator with sub_agents for delegation",
  workflow_agent: "Sequential or parallel task execution",
  tool_agent: "Agent specialized for specific tool operations"
};

// 2. Google Cloud Native Integration
const cloud_integration = {
  authentication: "Service account and IAM-based access",
  deployment: "Cloud Run containers or Vertex AI Agent Engine",
  storage: "Cloud Storage for state and artifacts",
  monitoring: "Cloud Logging and Cloud Monitoring integration"
};

// 3. Model and Tool Management
const framework_patterns = {
  model_selection: "Environment-based model configuration",
  tool_registration: "Decorator-based tool creation and assignment",
  agent_coordination: "Parent-child relationships with sub_agents",
  evaluation: "Built-in agent evaluation and testing frameworks"
};

// 4. Development Workflow
const workflow_patterns = {
  local_development: "Poetry-based dependency management with .env",
  testing: "Agent behavior testing with mock responses",
  deployment: "Docker containerization for Cloud Run",
  monitoring: "Production logging and performance tracking"
};
```

## Implementation Blueprint

### Technology Research Phase (COMPLETED VIA WEB SEARCH)

**RESEARCH FINDINGS:**

**Core Framework Analysis:**
- Google ADK is an open-source, code-first Python toolkit for building AI agents
- Introduced at Google Cloud NEXT 2025 as the framework powering Google's internal agents
- Designed to make agent development feel like traditional software development
- Model-agnostic with support for Gemini, GPT-4o, Claude, Mistral via LiteLLM
- Multi-agent by design with hierarchical, sequential, and parallel coordination

**Development Workflow Analysis:**
- Installation: `pip install google-adk` for stable version
- Project structure: Poetry-based dependency management recommended
- Local development: Built-in developer UI for agent testing
- Testing: Agent evaluation frameworks with mock and real LLM testing
- Deployment: Cloud Run containers or Vertex AI Agent Engine

**Best Practices Investigation:**
- Agent specialization: Create focused agents for specific tasks
- Tool integration: Use built-in tools (search, code execution) and custom functions
- Multi-agent coordination: Use sub_agents for delegation and orchestration
- Google Cloud integration: Service accounts, IAM roles, and native service usage
- Cost optimization: Model selection and usage monitoring for production

### Template Package Generation (IMPLEMENTATION PLAN)

```yaml
Generation Task 1 - Create Google ADK Template Directory Structure:
  CREATE complete use case directory structure:
    - use-cases/google-adk/
    - .claude/commands/ with ADK-specific PRP commands
    - PRPs/templates/ with ADK-specialized base template
    - PRPs/ai_docs/ with agent architecture documentation
    - examples/ with comprehensive agent implementations
    - All required subdirectories per template package requirements

Generation Task 2 - Generate ADK-Specific CLAUDE.md:
  CREATE Google ADK global rules file:
    - ADK-specific tooling (pip install google-adk, Poetry management)
    - Agent development patterns and architectural conventions
    - Google Cloud integration procedures and authentication
    - Multi-agent coordination patterns and best practices
    - Tool creation and integration standards
    - Agent evaluation and testing methodologies
    - Production deployment patterns for Cloud Run and Vertex AI

Generation Task 3 - Create Specialized ADK PRP Commands:
  GENERATE ADK domain-specific slash commands:
    - generate-google-adk-prp.md with agent research patterns
    - execute-google-adk-prp.md with ADK validation loops
    - Commands reference ADK-specific patterns from research
    - Include web search strategies for agent development

Generation Task 4 - Develop ADK-Specific Base PRP Template:
  CREATE specialized prp_google_adk_base.md template:
    - Pre-filled with ADK context from web research
    - Agent-specific success criteria and validation gates
    - Google Cloud documentation references
    - Multi-agent coordination patterns and validation loops
    - Tool integration and testing requirements

Generation Task 5 - Create Comprehensive ADK Examples:
  GENERATE working agent examples:
    - basic_chat_agent/ - Simple conversational agent with Gemini
    - search_assistant_agent/ - Tool-enabled agent with Google Search
    - multi_agent_system/ - Coordinator with specialized sub-agents
    - workflow_agents/ - Sequential and parallel agent workflows
    - cloud_run_deployment/ - Container deployment example
    - vertex_ai_integration/ - Vertex AI Agent Engine deployment
    - Each example includes working code, configuration, and documentation

Generation Task 6 - Create ADK Documentation:
  CREATE comprehensive ai_docs/ directory:
    - adk_architecture_patterns.md - Agent design patterns and best practices
    - multi_agent_coordination.md - Complex agent orchestration patterns
    - google_cloud_integration.md - Cloud service integration and deployment
    - All documentation based on web research findings

Generation Task 7 - Create Template Copy Script:
  CREATE Python script for template deployment:
    - copy_template.py with target directory argument
    - Copies complete Google ADK template structure
    - Includes all files: CLAUDE.md, commands, PRPs, examples, docs
    - Error handling and success feedback

Generation Task 8 - Generate Comprehensive README:
  CREATE comprehensive Google ADK README.md:
    - Clear description of Google ADK template purpose
    - Prominent copy script usage instructions
    - 3-step PRP framework workflow explanation
    - Template structure overview with all components
    - Quick start guide with concrete ADK examples
    - Agent development patterns and best practices
```

### Google Cloud Integration Details

```yaml
AUTHENTICATION_SETUP:
  service_account:
    - Create service account for agent applications
    - Configure IAM roles for required Google Cloud services
    - Download service account key for local development
    - Set GOOGLE_APPLICATION_CREDENTIALS environment variable

  vertex_ai_access:
    - Enable Vertex AI API in Google Cloud project
    - Configure model access permissions
    - Set up billing and usage monitoring
    - Configure regional model availability

DEPLOYMENT_PATTERNS:
  cloud_run:
    - Dockerfile for containerizing ADK agents
    - Cloud Run service configuration
    - Environment variable management
    - Auto-scaling and resource limits
    - Custom domain and HTTPS setup

  vertex_ai_agent_engine:
    - Agent Engine deployment configuration
    - Integration with Vertex AI models
    - Production monitoring and logging
    - Cost optimization strategies
```

### ADK Development Standards

```python
# Standard ADK Agent Structure
class StandardADKAgent:
    """Template for ADK agent implementation"""
    
    def __init__(self):
        self.agent_config = {
            "name": "agent_name",
            "model": "gemini-2.0-flash",  # Default to Gemini
            "instruction": "Clear, specific agent instructions",
            "description": "What this agent does",
            "tools": []  # List of tools for this agent
        }
    
    def setup_environment(self):
        """Environment configuration patterns"""
        return {
            "google_cloud_project": "from environment",
            "vertex_ai_location": "us-central1",
            "service_account_path": ".gcp/service-account.json",
            "model_configuration": "environment-based selection"
        }
    
    def create_tools(self):
        """Tool creation and registration patterns"""
        @tool
        def custom_tool(parameter: str) -> str:
            """Tool implementation with proper typing"""
            return f"Tool result for {parameter}"
        
        return [custom_tool]
    
    def setup_multi_agent(self):
        """Multi-agent coordination patterns"""
        sub_agents = [
            LlmAgent(name="specialist1", model="gemini-2.0-flash"),
            LlmAgent(name="specialist2", model="gemini-2.0-flash")
        ]
        
        coordinator = LlmAgent(
            name="coordinator",
            model="gemini-2.0-flash",
            sub_agents=sub_agents
        )
        
        return coordinator
```

## Validation Loop

### Level 1: Template Structure Validation

```bash
# CRITICAL: Verify complete Google ADK template package structure
find use-cases/google-adk -type f | sort
ls -la use-cases/google-adk/.claude/commands/
ls -la use-cases/google-adk/PRPs/templates/
ls -la use-cases/google-adk/examples/

# Verify ADK-specific content
grep -r "google-adk\|ADK\|Agent" use-cases/google-adk/ | wc -l
test -f use-cases/google-adk/copy_template.py

# Expected: All required files present with ADK-specific content
# If missing: Generate missing files following ADK patterns
```

### Level 2: ADK Content Quality Validation

```bash
# Verify ADK-specific content accuracy
grep -r "TODO\|PLACEHOLDER\|{technology}" use-cases/google-adk/
grep -r "google.adk" use-cases/google-adk/examples/ | wc -l
grep -r "gemini-2.0-flash" use-cases/google-adk/ | wc -l

# Check for agent patterns
grep -r "LlmAgent\|Agent\|sub_agents" use-cases/google-adk/
grep -r "google_search\|@tool" use-cases/google-adk/examples/

# Expected: No placeholder content, ADK patterns present
# If issues: Research and add proper ADK-specific content
```

### Level 3: ADK Functional Validation

```bash
# Test ADK template functionality
cd use-cases/google-adk

# Test ADK PRP generation command
/generate-google-adk-prp INITIAL.md
ls PRPs/*.md | grep google-adk

# Test example agent code
cd examples/basic_chat_agent
python -c "import google.adk.agents; print('ADK import successful')"

# Expected: PRP generation works, examples import successfully
# If failing: Debug ADK command patterns and example code
```

### Level 4: Google Cloud Integration Testing

```bash
# Verify Google Cloud integration patterns
grep -r "vertex-ai\|cloud-run\|gcloud" use-cases/google-adk/
grep -r "GOOGLE_APPLICATION_CREDENTIALS" use-cases/google-adk/
grep -r "service_account" use-cases/google-adk/examples/

# Test deployment configurations
find use-cases/google-adk -name "Dockerfile" -o -name "*.yaml" -o -name "requirements.txt"

# Expected: Google Cloud patterns present, deployment configs exist
# If issues: Add proper Google Cloud integration documentation
```

## Final Validation Checklist

### Template Package Completeness

- [ ] Complete directory structure: `tree use-cases/google-adk`
- [ ] All required files present: CLAUDE.md, commands, base PRP, examples, ai_docs
- [ ] Copy script present: `copy_template.py` with proper functionality
- [ ] README comprehensive: Includes copy script instructions and ADK workflow
- [ ] ADK-specific content: Agent patterns accurately represented
- [ ] Working examples: All agent examples use proper ADK imports and patterns
- [ ] Google Cloud integration: Deployment and authentication patterns included

### Quality and ADK Specialization

- [ ] No placeholder content: `grep -r "TODO\|PLACEHOLDER"`
- [ ] ADK specialization: Agent development patterns properly documented
- [ ] Google Cloud native: Vertex AI and Cloud Run integration included
- [ ] Multi-agent patterns: Complex coordination examples provided
- [ ] Tool integration: Built-in and custom tool patterns documented
- [ ] Production ready: Deployment, monitoring, and cost optimization included

### Framework Integration

- [ ] Inherits base principles: Context engineering workflow preserved
- [ ] Proper ADK specialization: Agent-specific patterns included
- [ ] Command compatibility: ADK slash commands work as expected
- [ ] Documentation consistency: Follows established documentation patterns
- [ ] Maintainable structure: Easy to update as ADK evolves

---

## Anti-Patterns to Avoid

### ADK Template Generation

- ❌ Don't create generic agent templates - research ADK-specific patterns deeply
- ❌ Don't skip Google Cloud integration - ADK is designed for Google Cloud deployment
- ❌ Don't ignore multi-agent patterns - ADK's strength is complex agent coordination
- ❌ Don't use placeholder content - include real ADK code and configurations

### Agent Development Quality

- ❌ Don't assume knowledge - document ADK-specific patterns explicitly
- ❌ Don't skip tool integration - include comprehensive tool creation patterns
- ❌ Don't ignore Google Cloud auth - include proper service account and IAM patterns
- ❌ Don't forget cost optimization - include monitoring and cost control strategies

### Framework Integration

- ❌ Don't break base patterns - maintain compatibility with context engineering principles
- ❌ Don't duplicate effort - reuse and extend base framework components appropriately
- ❌ Don't ignore consistency - follow established naming and structure conventions
- ❌ Don't skip validation - ensure ADK templates actually work with real Google Cloud services

**Confidence Score: 9/10** - Comprehensive research completed on Google ADK with official documentation, examples, and integration patterns. Ready to generate immediately usable template package for sophisticated agent development.