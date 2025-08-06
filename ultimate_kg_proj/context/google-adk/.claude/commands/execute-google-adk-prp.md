# Execute Google ADK Agent PRP

Execute a comprehensive Google ADK agent development PRP to create complete AI agent systems and multi-agent architectures using Google's Agent Development Kit.

## PRP File: $ARGUMENTS

## Execution Process

1. **Load Agent Development PRP**
   - Read the specified Google ADK agent PRP file completely
   - Understand the target agent system and all multi-agent coordination requirements
   - Review all web research findings documented in the PRP
   - Follow all instructions for agent system implementation

2. **ULTRATHINK - Agent System Design**
   - Create comprehensive agent implementation plan
   - Plan the complete agent system architecture based on PRP research
   - Design multi-agent coordination and delegation patterns
   - Map agent requirements to Google ADK capabilities
   - Plan all required files, configurations, and their relationships

3. **Implement Complete Agent System**
   - Create agent project structure with proper organization
   - Implement individual agents with clear instructions and tools
   - Create multi-agent coordination and workflow patterns
   - Develop custom tools and integrate built-in ADK tools
   - Configure Google Cloud integration for deployment

4. **Validate Agent System**
   - Run all validation commands specified in the PRP
   - Test individual agent functionality and responses
   - Validate multi-agent coordination and communication
   - Test Google Cloud integration and authentication
   - Verify agent system completeness and accuracy

5. **Quality Assurance**
   - Ensure agents follow all Google ADK best practices
   - Verify multi-agent patterns are properly implemented
   - Check validation loops are appropriate and executable for agents
   - Confirm agent system is production-ready for deployment

6. **Complete Implementation**
   - Review agent system against all PRP requirements
   - Ensure all success criteria from the PRP are met
   - Validate agent system is ready for Google Cloud deployment

## Agent System Requirements

Create a complete agent system with this structure:

### Required Project Structure
```
agents/
├── __init__.py
├── main_agent.py                    # Primary coordinator agent
├── specialized_agents/              # Individual specialized agents
│   ├── __init__.py
│   ├── search_agent.py
│   ├── task_agent.py
│   └── coordination_agent.py
└── multi_agent_system.py           # Multi-agent coordination logic

tools/
├── __init__.py
├── custom_tools.py                  # Custom tool implementations
└── tool_registry.py                # Tool registration and management

configs/
├── __init__.py
├── agent_config.py                  # Agent configuration management
├── environment.py                   # Environment and Google Cloud setup
└── deployment_config.py            # Cloud Run and Vertex AI configs

deployments/
├── Dockerfile                       # Container deployment
├── cloud_run.yaml                   # Cloud Run service configuration
├── vertex_ai_config.json           # Vertex AI Agent Engine config
└── requirements.txt                 # Python dependencies

tests/
├── __init__.py
├── test_agents.py                   # Agent behavior testing
├── test_multi_agent.py              # Multi-agent coordination tests
└── test_tools.py                    # Tool functionality tests

.env.example                         # Environment variable template
README.md                           # Project documentation
pyproject.toml                      # Poetry dependency management
```

### Implementation Requirements Based on PRP Research

**Agent Implementation** must include:
- Individual agent classes with clear instructions and responsibilities
- Multi-agent coordinator with proper sub-agent delegation
- Custom tool integration with @tool decorator
- Built-in Google ADK tool usage (google_search, code_execution)
- Proper error handling and retry mechanisms

**Google Cloud Integration** must include:
- Service account authentication configuration
- Vertex AI model integration and configuration
- Cloud Run deployment setup with proper scaling
- Environment-based configuration management
- Cost monitoring and optimization strategies

**Testing and Validation** must include:
- Agent behavior testing with mock and real responses
- Multi-agent coordination validation
- Tool functionality and error handling tests
- Google Cloud integration testing
- Production readiness validation

## Validation Requirements

### Agent System Validation
```bash
# Verify complete agent structure exists
find . -name "*.py" -type f | sort
ls -la agents/ tools/ configs/ deployments/

# Check required files exist
test -f agents/main_agent.py
test -f tools/custom_tools.py
test -f configs/agent_config.py
test -f deployments/Dockerfile
test -f pyproject.toml

# Test Python imports and syntax
python -m py_compile agents/*.py tools/*.py configs/*.py
python -c "from google.adk.agents import Agent, LlmAgent; print('ADK imports successful')"
```

### Agent Functionality Validation
```bash
# Test agent creation and basic functionality
python -c "
from agents.main_agent import create_main_agent
agent = create_main_agent()
print(f'Agent created: {agent.name}')
"

# Test multi-agent coordination
python -c "
from agents.multi_agent_system import create_multi_agent_system
system = create_multi_agent_system()
print(f'Multi-agent system: {len(system.sub_agents)} agents')
"

# Test custom tools
python -c "
from tools.custom_tools import *
print('Custom tools imported successfully')
"
```

### Google Cloud Integration Validation
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
test -f deployments/Dockerfile && echo "Docker config present" || echo "Docker config missing"
test -f deployments/cloud_run.yaml && echo "Cloud Run config present" || echo "Cloud Run config missing"
```

## Success Criteria

- [ ] Complete agent system structure created exactly as specified
- [ ] All required agent files present and properly implemented
- [ ] Multi-agent coordination patterns working correctly
- [ ] Custom and built-in tools properly integrated
- [ ] Google Cloud integration configured and tested
- [ ] Agent system follows all Google ADK best practices
- [ ] Validation loops appropriate and executable for agent development
- [ ] Agent system immediately deployable to Google Cloud
- [ ] All web research findings from PRP properly implemented
- [ ] Testing framework comprehensive and agent-specific
- [ ] Documentation complete with deployment instructions
- [ ] Cost optimization and monitoring strategies implemented

Note: If any validation fails, analyze the error, fix the agent system components, and re-validate until all criteria pass. The agent system must be production-ready and immediately deployable to Google Cloud Platform.