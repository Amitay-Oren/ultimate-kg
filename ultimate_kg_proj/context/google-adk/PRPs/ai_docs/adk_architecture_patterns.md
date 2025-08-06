# Google ADK Architecture Patterns

This document outlines the core architectural patterns and best practices for building AI agents and multi-agent systems using Google's Agent Development Kit (ADK).

## Agent Creation Patterns

### Basic Agent Pattern
```python
from google.adk.agents import Agent
from google.adk.tools import google_search

# Simple agent with built-in tools
basic_agent = Agent(
    name="search_assistant",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant. Answer questions using Google Search.",
    description="An assistant that can search the web.",
    tools=[google_search]
)
```

### LLM Agent Pattern
```python
from google.adk.agents import LlmAgent

# More advanced agent with custom configuration
advanced_agent = LlmAgent(
    name="task_specialist",
    model="gemini-2.0-flash",
    instruction="You are a task specialist. Complete tasks efficiently and accurately.",
    description="Specialized agent for complex task execution"
)
```

### Custom Tool Integration
```python
from google.adk.tools import tool

@tool
def currency_converter(from_currency: str, to_currency: str, amount: float) -> str:
    """Convert currency amounts between different currencies."""
    # Implementation here
    rate = get_exchange_rate(from_currency, to_currency)
    converted = amount * rate
    return f"{amount} {from_currency} = {converted:.2f} {to_currency}"

# Agent with custom tools
finance_agent = Agent(
    name="finance_assistant",
    model="gemini-2.0-flash",
    instruction="You help with financial calculations and currency conversions.",
    tools=[currency_converter]
)
```

## Multi-Agent Coordination Patterns

### Hierarchical Pattern
```python
from google.adk.agents import LlmAgent

# Individual specialized agents
greeter = LlmAgent(
    name="greeter",
    model="gemini-2.0-flash",
    instruction="Greet users warmly and professionally."
)

task_executor = LlmAgent(
    name="task_executor",
    model="gemini-2.0-flash", 
    instruction="Execute specific tasks assigned by the coordinator."
)

# Coordinator with sub-agents
coordinator = LlmAgent(
    name="coordinator",
    model="gemini-2.0-flash",
    description="I coordinate greetings and task execution.",
    sub_agents=[greeter, task_executor]
)
```

### Sequential Workflow Pattern
```python
# Agent for sequential task processing
sequential_agent = LlmAgent(
    name="workflow_processor",
    model="gemini-2.0-flash",
    instruction="Process tasks in sequence, ensuring each step completes before the next.",
    sub_agents=[
        data_collector,
        data_processor, 
        report_generator
    ]
)
```

### Parallel Coordination Pattern
```python
# Agent for parallel task processing
parallel_coordinator = LlmAgent(
    name="parallel_processor",
    model="gemini-2.0-flash",
    instruction="Coordinate multiple agents working on different aspects of the same problem.",
    sub_agents=[
        research_agent,
        analysis_agent,
        writing_agent
    ]
)
```

## Agent Configuration Patterns

### Environment-Based Configuration
```python
import os
from dotenv import load_dotenv

load_dotenv()

def create_configured_agent(name: str, instruction: str):
    """Create agent with environment-based configuration."""
    return Agent(
        name=name,
        model=os.getenv("ADK_MODEL", "gemini-2.0-flash"),
        instruction=instruction
    )

# Usage
agent = create_configured_agent(
    name="customer_service",
    instruction="Provide excellent customer service support."
)
```

### Dynamic Agent Creation
```python
def create_specialist_agent(domain: str, capabilities: list):
    """Dynamically create specialized agents based on domain."""
    
    instruction = f"You are a {domain} specialist. Your capabilities include: {', '.join(capabilities)}"
    
    return LlmAgent(
        name=f"{domain}_specialist",
        model="gemini-2.0-flash",
        instruction=instruction,
        description=f"Specialized agent for {domain} tasks"
    )

# Create domain-specific agents
marketing_agent = create_specialist_agent(
    "marketing", 
    ["content creation", "campaign analysis", "social media management"]
)
```

## Tool Orchestration Patterns

### Tool Chaining
```python
@tool
def research_topic(topic: str) -> str:
    """Research a topic and return key findings."""
    # Implementation
    return f"Research findings for {topic}"

@tool
def analyze_findings(findings: str) -> str:
    """Analyze research findings and extract insights."""
    # Implementation
    return f"Analysis of: {findings}"

@tool
def generate_report(analysis: str) -> str:
    """Generate a comprehensive report from analysis."""
    # Implementation
    return f"Report based on: {analysis}"

# Agent with chained tools
research_agent = Agent(
    name="research_analyst",
    model="gemini-2.0-flash",
    instruction="Research topics, analyze findings, and generate comprehensive reports.",
    tools=[research_topic, analyze_findings, generate_report]
)
```

### Conditional Tool Usage
```python
@tool
def check_data_quality(data: str) -> dict:
    """Check data quality and return status."""
    quality_score = assess_quality(data)
    return {
        "score": quality_score,
        "needs_cleaning": quality_score < 0.8,
        "recommendations": get_quality_recommendations(quality_score)
    }

@tool 
def clean_data(data: str) -> str:
    """Clean data based on quality assessment."""
    # Implementation
    return cleaned_data

# Agent with conditional tool logic
data_agent = Agent(
    name="data_processor",
    model="gemini-2.0-flash",
    instruction="Process data, check quality, and clean if necessary.",
    tools=[check_data_quality, clean_data]
)
```

## Error Handling Patterns

### Graceful Tool Failure
```python
@tool
def robust_api_call(endpoint: str, params: dict) -> str:
    """Make API call with comprehensive error handling."""
    try:
        response = make_api_request(endpoint, params)
        return f"Success: {response}"
    except TimeoutError:
        return "Error: API request timed out. Please try again later."
    except ConnectionError:
        return "Error: Unable to connect to API. Check network connection."
    except Exception as e:
        return f"Error: Unexpected issue occurred - {str(e)}"

# Agent with robust error handling
api_agent = Agent(
    name="api_specialist",
    model="gemini-2.0-flash",
    instruction="Make API calls and handle errors gracefully.",
    tools=[robust_api_call]
)
```

### Agent Fallback Patterns
```python
# Primary agent with fallback capability
primary_agent = LlmAgent(
    name="primary_processor",
    model="gemini-2.0-flash",
    instruction="Handle requests efficiently. If you cannot complete a task, explain why."
)

# Fallback agent for when primary fails
fallback_agent = LlmAgent(
    name="fallback_processor", 
    model="gemini-2.0-flash",
    instruction="Handle requests that the primary agent could not complete."
)

# Coordinator with fallback logic
resilient_coordinator = LlmAgent(
    name="resilient_system",
    model="gemini-2.0-flash",
    instruction="Try primary agent first, use fallback if primary fails.",
    sub_agents=[primary_agent, fallback_agent]
)
```

## State Management Patterns

### Agent Context Sharing
```python
class SharedContext:
    """Shared context for multi-agent coordination."""
    def __init__(self):
        self.conversation_history = []
        self.current_task = None
        self.completed_tasks = []
        self.shared_data = {}

# Agents that share context
context = SharedContext()

agent_a = create_context_aware_agent("agent_a", context)
agent_b = create_context_aware_agent("agent_b", context)

coordinator = LlmAgent(
    name="context_coordinator",
    model="gemini-2.0-flash",
    instruction="Coordinate agents while maintaining shared context.",
    sub_agents=[agent_a, agent_b]
)
```

### Persistent State Management
```python
import json

@tool
def save_agent_state(agent_name: str, state_data: dict) -> str:
    """Save agent state to persistent storage."""
    with open(f"states/{agent_name}_state.json", "w") as f:
        json.dump(state_data, f)
    return f"State saved for {agent_name}"

@tool
def load_agent_state(agent_name: str) -> dict:
    """Load agent state from persistent storage."""
    try:
        with open(f"states/{agent_name}_state.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Agent with state persistence
stateful_agent = Agent(
    name="stateful_processor",
    model="gemini-2.0-flash",
    instruction="Maintain state across interactions using save/load functions.",
    tools=[save_agent_state, load_agent_state]
)
```

## Performance Optimization Patterns

### Model Selection Strategy
```python
def select_optimal_model(task_complexity: str, budget: str) -> str:
    """Select optimal model based on task and budget constraints."""
    
    if task_complexity == "simple" and budget == "low":
        return "gemini-2.0-flash"
    elif task_complexity == "complex" and budget == "high":
        return "gemini-2.0-pro"
    else:
        return "gemini-2.0-flash"  # Default choice

# Dynamic model selection
adaptive_agent = Agent(
    name="adaptive_processor",
    model=select_optimal_model("complex", "medium"),
    instruction="Adapt processing approach based on task complexity."
)
```

### Caching and Optimization
```python
from functools import lru_cache

@lru_cache(maxsize=100)
@tool
def cached_computation(input_data: str) -> str:
    """Perform expensive computation with caching."""
    # Expensive operation here
    result = perform_complex_analysis(input_data)
    return result

# Agent with optimized tools
optimized_agent = Agent(
    name="optimized_processor", 
    model="gemini-2.0-flash",
    instruction="Perform computations efficiently using cached results when possible.",
    tools=[cached_computation]
)
```

## Integration Patterns Summary

- **Agent Specialization**: Create focused agents for specific domains
- **Hierarchical Coordination**: Use parent-child relationships for complex workflows  
- **Tool Orchestration**: Chain and coordinate tools for comprehensive functionality
- **Error Resilience**: Implement comprehensive error handling and fallback mechanisms
- **State Management**: Share context and maintain persistence across agent interactions
- **Performance Optimization**: Select appropriate models and implement caching strategies

These patterns provide a foundation for building sophisticated, scalable, and robust agent systems using Google's Agent Development Kit.