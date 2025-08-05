# Google Agent Development Kit (ADK) Context Engineering Template

A comprehensive template for building production-grade AI agents, multi-agent systems, and complex agentic workflows using Google's Agent Development Kit with context engineering best practices, Google Cloud integration, and comprehensive deployment patterns.

## 🚀 Quick Start - Copy Template

**Get started in 2 minutes:**

```bash
# 1. Copy this template to your new project
python copy_template.py /path/to/my-agent-project

# 2. Navigate to your project
cd /path/to/my-agent-project

# 3. Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your Google Cloud configuration

# 5. Define your agent requirements
# Edit PRPs/INITIAL.md with your specific agent needs

# 6. Generate and execute PRP for your agent system
/generate-google-adk-prp PRPs/INITIAL.md
/execute-google-adk-prp PRPs/generated-agent-prp.md
```

## 📖 What is This Template?

This template provides everything you need to build sophisticated AI agents using Google's Agent Development Kit with proven context engineering workflows. It combines:

- **Google ADK Best Practices**: Multi-agent coordination, tool integration, and Google Cloud deployment
- **Context Engineering Workflows**: Proven PRP (Product Requirements Prompts) methodology
- **Working Examples**: Complete agent implementations from basic to complex multi-agent systems
- **Production Deployment**: Cloud Run and Vertex AI deployment patterns

## 🎯 PRP Framework Workflow

This template uses a 3-step context engineering workflow for building AI agent systems:

### 1. **Define Agent Requirements** (`PRPs/INITIAL.md`)
Start by clearly defining what your agent system needs to do:
```markdown
# Customer Support Agent System - Initial Requirements

## Overview
Build an intelligent multi-agent customer support system that can handle 
inquiries, access customer data, and coordinate between specialized agents.

## Core Requirements
- Multi-agent coordination with specialized roles
- Customer authentication and account access
- Search and knowledge base integration
- Escalation workflows and human handoff
- Google Cloud deployment and scaling
...
```

### 2. **Generate Implementation Plan** 
```bash
/generate-google-adk-prp PRPs/INITIAL.md
```
This creates a comprehensive 'Product Requirements Prompts' document that includes:
- Google ADK technology research and agent architecture patterns
- Multi-agent system design with coordination strategies
- Implementation roadmap with Google Cloud integration
- Security patterns and production deployment considerations

### 3. **Execute Implementation**
```bash
/execute-google-adk-prp PRPs/your_agent_system.md
```
This implements the complete agent system based on the PRP, including:
- Individual specialized agents with clear responsibilities
- Multi-agent coordinator with proper delegation patterns
- Tool integration with comprehensive error handling
- Google Cloud deployment configuration and monitoring

## 📂 Template Structure

```
google-adk/
├── CLAUDE.md                           # Google ADK global development rules
├── copy_template.py                    # Template deployment script
├── .claude/commands/
│   ├── generate-google-adk-prp.md      # PRP generation for agents
│   └── execute-google-adk-prp.md       # PRP execution for agents
├── PRPs/
│   ├── templates/
│   │   └── prp_google_adk_base.md      # Base PRP template for agents
│   ├── ai_docs/                        # ADK documentation and patterns
│   │   ├── adk_architecture_patterns.md
│   │   ├── multi_agent_coordination.md
│   │   └── google_cloud_integration.md
│   └── INITIAL.md                      # Example agent requirements
├── examples/
│   ├── basic_chat_agent/               # Simple conversational agent
│   ├── search_assistant_agent/         # Tool-enabled agent with search
│   ├── multi_agent_system/             # Complex agent coordination
│   ├── workflow_agents/                # Sequential/parallel workflows
│   ├── cloud_run_deployment/           # Cloud Run deployment example
│   └── vertex_ai_integration/          # Vertex AI Agent Engine example
└── README.md                           # This file
```

## 🤖 Agent Examples Included

### 1. Basic Chat Agent (`examples/basic_chat_agent/`)
A simple conversational agent demonstrating core Google ADK patterns:
- **Environment-based model configuration** (Gemini 2.0 Flash)
- **Simple conversation handling** with natural interaction patterns
- **Error handling and recovery** for robust operation
- **Clean, minimal implementation** following ADK best practices

**Key Features:**
- Gemini model integration with environment configuration
- Natural conversation flow with user input validation
- Graceful error handling and recovery mechanisms
- Simple setup and execution for learning ADK basics

### 2. Search Assistant Agent (`examples/search_assistant_agent/`)
An agent with Google Search integration capabilities:
- **Built-in tool integration** (google_search from ADK)
- **Information gathering and synthesis** from web sources
- **Context-aware responses** based on search results
- **Error handling for search failures** and fallback mechanisms

**Key Features:**
- Google Search tool integration for information retrieval
- Intelligent response generation based on search results
- Handling of search API failures and rate limiting
- Context preservation across multiple search queries

### 3. Multi-Agent System (`examples/multi_agent_system/`)
**The canonical reference implementation** showing proper multi-agent coordination:
- **Hierarchical agent coordination** with clear delegation patterns
- **Specialized agent roles** (coordinator, search, task execution)
- **Inter-agent communication** and state sharing
- **Comprehensive error handling** across agent interactions

**Key Features:**
- Parent coordinator with specialized sub-agents
- Dynamic task routing based on request type
- Shared context and state management across agents
- Fallback mechanisms when individual agents fail

### 4. Workflow Agents (`examples/workflow_agents/`)
Demonstrates sequential and parallel agent workflow patterns:
- **Sequential processing** for step-by-step task completion
- **Parallel coordination** for concurrent task execution
- **Workflow state management** across multiple processing steps
- **Error recovery and retry mechanisms** for workflow resilience

**Key Features:**
- Sequential workflow for dependent task processing
- Parallel workflow for independent task coordination
- State persistence across workflow steps
- Comprehensive error handling and recovery strategies

### 5. Cloud Run Deployment (`examples/cloud_run_deployment/`)
**Production deployment example** for Google Cloud:
- **Docker containerization** for consistent deployment
- **Cloud Run service configuration** with auto-scaling
- **Environment variable management** for production secrets
- **Health checks and monitoring** for production reliability

**Key Features:**
- Complete Dockerfile for agent containerization
- Cloud Run YAML configuration with resource limits
- Service account and IAM configuration
- Production monitoring and logging setup

### 6. Vertex AI Integration (`examples/vertex_ai_integration/`)
Shows integration with Vertex AI Agent Engine:
- **Vertex AI model integration** for production LLM access
- **Agent Engine deployment** for managed agent hosting
- **Cost optimization strategies** for production usage
- **Regional deployment** and model availability management

**Key Features:**
- Vertex AI model configuration and access patterns
- Agent Engine deployment and management
- Cost monitoring and budget controls
- Regional optimization for latency and availability

## 🎯 What You Can Build

This template enables you to create sophisticated agent systems including:

### Customer Service Systems
- Multi-agent customer support with specialized roles
- Automated ticket routing and escalation
- Knowledge base integration and search
- Human handoff workflows

### Research and Analysis Platforms
- Multi-agent research coordination
- Automated data gathering and analysis
- Report generation and insight synthesis
- Real-time information processing

### Task Automation Systems
- Complex workflow orchestration
- Multi-step process automation
- Error handling and recovery mechanisms
- Integration with external systems and APIs

### Content Creation Platforms
- Multi-agent content development
- Research, writing, and editing coordination
- Quality assurance and review processes
- Multi-format content generation

## 📚 Key Features

### Google ADK Integration
- **Agent Creation**: Simple and advanced agent creation patterns
- **Multi-Agent Coordination**: Hierarchical, sequential, and parallel patterns
- **Tool Integration**: Built-in tools (search, code execution) and custom tools
- **Model Flexibility**: Support for Gemini, GPT-4o, Claude, Mistral via LiteLLM

### Google Cloud Native
- **Vertex AI Integration**: Production-grade model access and management
- **Cloud Run Deployment**: Scalable serverless agent hosting
- **Authentication**: Service account and IAM configuration
- **Cost Optimization**: Resource limits, quotas, and monitoring

### Production Ready
- **Comprehensive Testing**: Agent behavior and coordination validation
- **Error Handling**: Robust failure recovery and retry mechanisms
- **Monitoring**: Logging, metrics, and alerting for production operations
- **Security**: Input validation, access controls, and audit logging

### Context Engineering Integration
- **PRP Framework**: Proven methodology for complex agent development
- **Validation Loops**: Comprehensive testing and quality assurance
- **Documentation**: Complete patterns and best practices
- **Rapid Development**: Template-based project initialization

## 🔍 Examples Walkthrough

### Running the Basic Chat Agent
```bash
cd examples/basic_chat_agent
python agent.py

# Example conversation:
# You: What's the weather like?
# Agent: I'd be happy to help you with weather information! However, I don't have access to real-time weather data...
```

### Testing Multi-Agent Coordination
```bash
cd examples/multi_agent_system
python multi_agent_demo.py

# Watch agents coordinate:
# Coordinator: Routing search request to search specialist...
# Search Agent: Found 10 results for your query...
# Coordinator: Synthesizing results from search agent...
```

### Deploying to Cloud Run
```bash
cd examples/cloud_run_deployment
docker build -t my-agent-system .
gcloud run deploy agent-system --image my-agent-system --region us-central1
```

## 📖 Documentation References

- **Official Google ADK Documentation**: https://google.github.io/adk-docs/
- **Google ADK Python Repository**: https://github.com/google/adk-python
- **Google ADK Samples**: https://github.com/google/adk-samples
- **Vertex AI Documentation**: https://cloud.google.com/vertex-ai/docs
- **Cloud Run Documentation**: https://cloud.google.com/run/docs
- **Context Engineering Methodology**: See main repository README

## 🚫 Common Gotchas

### Google Cloud Authentication
- **Service Account Setup**: Ensure proper IAM roles for Vertex AI access
- **Regional Limitations**: Different models available in different regions
- **Credential Management**: Use environment variables, never hardcode keys
- **Local vs Production**: Different auth patterns for development and deployment

### Agent Coordination Complexity
- **Over-Complex Hierarchies**: Keep agent relationships simple and clear
- **State Management**: Properly share context between coordinating agents
- **Error Cascading**: One agent failure shouldn't break the entire system
- **Debugging Difficulty**: Complex multi-agent interactions can be hard to debug

### Cost Management
- **Model Usage Accumulation**: Monitor token usage across all agents
- **Regional Pricing Differences**: Choose regions based on cost and latency
- **Quota Management**: Set appropriate limits to prevent cost overruns
- **Development vs Production**: Use different cost controls for different environments

### Tool Integration Issues
- **Tool Timeout Handling**: Long-running tools may timeout in agent workflows
- **API Rate Limiting**: External APIs may limit request frequency
- **Error Propagation**: Tool failures should be handled gracefully by agents
- **Tool Orchestration**: Complex tool chains require careful error handling

## 🆘 Support & Contributing

- **Issues**: Report problems with the template or examples
- **Improvements**: Contribute additional agent patterns or Google Cloud integrations
- **Questions**: Ask about Google ADK integration or multi-agent coordination

This template is part of the larger Context Engineering framework. See the main repository for more context engineering templates and methodologies.

---

**Ready to build production-grade AI agents?** Start with `python copy_template.py my-agent-project` and follow the PRP workflow! 🚀