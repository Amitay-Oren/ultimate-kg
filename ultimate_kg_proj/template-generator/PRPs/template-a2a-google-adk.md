---
name: "A2A-Compatible Google ADK Template Generator"
description: "Complete context engineering template for building A2A-compatible AI agents using Google Agent Development Kit with cross-platform interoperability"
---

## Purpose

Generate a comprehensive context engineering template package for building A2A (Agent-to-Agent) protocol compatible AI agents using Google's Agent Development Kit. This template enables developers to create production-ready agents that can seamlessly communicate and collaborate across different AI platforms (LangGraph, CrewAI, Semantic Kernel, etc.) while leveraging Google Cloud infrastructure.

## Core Principles

1. **A2A Protocol Compliance**: Full adherence to Agent-to-Agent protocol specifications for cross-platform interoperability
2. **Google Cloud Integration**: Native integration with Vertex AI, Cloud Run, and Google Cloud services
3. **Cross-Platform Collaboration**: Enable agents to delegate tasks and coordinate with agents from other frameworks
4. **Production-Ready Architecture**: Enterprise-grade patterns for deployment, monitoring, and scaling
5. **Security-First Design**: Comprehensive security patterns for inter-agent communication and trust

---

## Goal

Generate a complete A2A-compatible Google ADK template package that includes:

- A2A protocol implementation patterns with Google ADK
- Cross-platform agent communication and coordination
- Google Cloud deployment and scaling patterns
- Comprehensive security and authentication mechanisms
- Production-ready agent architecture templates
- Testing and validation frameworks for A2A compliance

## Why

- **Cross-Platform Interoperability**: Enable Google ADK agents to work with agents from any platform
- **Enterprise Integration**: Provide production-ready patterns for enterprise A2A agent networks
- **Developer Productivity**: Accelerate development of A2A-compatible agents with proven patterns
- **Protocol Compliance**: Ensure adherence to A2A protocol specifications and best practices
- **Scalable Architecture**: Support for large-scale distributed agent systems

## What

### Template Package Components

**Complete Directory Structure:**
```
use-cases/a2a-google-adk/
├── CLAUDE.md                           # A2A-Google ADK implementation guide
├── .claude/commands/
│   ├── generate-a2a-google-adk-prp.md  # A2A-specific PRP generation
│   └── execute-a2a-google-adk-prp.md   # A2A-specific PRP execution
├── PRPs/
│   ├── templates/
│   │   └── prp_a2a_google_adk_base.md  # A2A-ADK base PRP template
│   ├── ai_docs/
│   │   ├── a2a_protocol_patterns.md    # A2A protocol implementation patterns
│   │   ├── google_adk_integration.md   # Google ADK with A2A integration
│   │   └── cross_platform_agent_coordination.md # Multi-platform agent patterns
│   └── INITIAL.md                      # Example A2A agent request
├── examples/
│   ├── basic_a2a_agent/               # Simple A2A-compatible agent
│   ├── a2a_server_setup/              # A2A server configuration
│   ├── cross_platform_delegation/     # Inter-platform task delegation
│   ├── multi_agent_coordination/      # A2A agent network coordination
│   ├── google_cloud_deployment/       # Cloud Run deployment patterns
│   └── a2a_testing_framework/         # A2A compliance testing
├── config/
│   ├── a2a_server_config.py           # A2A server configuration
│   ├── google_cloud_config.py         # Google Cloud integration
│   └── agent_registry.py              # Agent discovery and registration
├── copy_template.py                   # Template deployment script
└── README.md                          # Comprehensive usage guide
```

**A2A Protocol Integration:**
- A2A server setup and agent registration patterns
- Cross-platform agent discovery and communication
- A2A-compliant task delegation and execution
- Inter-agent security and authentication
- Protocol compliance validation and testing

**Google ADK Specialization:**
- Vertex AI model integration within A2A framework
- Google Cloud deployment patterns for A2A agents
- ADK tool integration for A2A-compatible agents
- Google Cloud authentication and security
- Cloud Run scaling for A2A agent networks

### Success Criteria

- [ ] Complete A2A-Google ADK template package structure generated
- [ ] A2A protocol compliance patterns documented and implemented
- [ ] Google ADK integration with A2A protocol working examples
- [ ] Cross-platform agent communication examples included
- [ ] Google Cloud deployment patterns for A2A agents ready
- [ ] A2A server setup and configuration templates complete
- [ ] Agent discovery and registration patterns implemented
- [ ] Security and authentication patterns for A2A networks included
- [ ] Testing framework for A2A compliance validation ready
- [ ] Comprehensive documentation and usage examples complete

## All Needed Context

### A2A Protocol Foundation (RESEARCHED)

```yaml
# A2A PROTOCOL CORE - Based on provided links and research
- url: https://a2a-protocol.org/latest/
  findings: |
    A2A is an open standard for seamless AI agent communication across platforms.
    Key principles: Interoperability, cross-platform collaboration, security.
    Enables agents to delegate tasks, exchange information, coordinate actions.
    Works alongside MCP (Model Context Protocol) for complete agent ecosystems.

- url: https://a2a-protocol.org/latest/tutorials/python  
  findings: |
    Python implementation patterns for A2A protocol.
    Agent server architecture and setup procedures.
    Communication protocols and message handling.
    Integration patterns with different AI frameworks.

- url: https://github.com/a2aproject/a2a-python
  findings: |
    A2A Python SDK with Python 3.10+ requirement.
    Installation: uv add a2a-sdk or pip install a2a-sdk[grpc,telemetry]
    Core concept: Run agentic applications as A2AServers following A2A Protocol.
    Supports gRPC, telemetry, and database integrations.

- url: https://github.com/a2aproject/a2a-samples/tree/main/samples/python
  findings: |
    Python samples with agents/, hosts/, common/ structure.
    Multiple framework support (LangGraph examples included).
    CLI and web application host patterns.
    Orchestrator agent for task delegation.
    Python 3.13+ requirement, UV package management.
```

### Google ADK Integration Patterns

```yaml
# GOOGLE ADK FOUNDATION - From existing template analysis
- file: ../google-adk/CLAUDE.md
  why: Google ADK development patterns and cloud integration
  
- file: ../google-adk/examples/
  why: Working Google ADK agent implementations and patterns

- url: https://google.github.io/adk-docs/
  findings: |
    Google Agent Development Kit for flexible, modular AI agents.
    Support for Vertex AI models (Gemini, PaLM).
    Workflow orchestration (Sequential, Parallel, Loop agents).
    Tool ecosystem integration and custom function development.

- url: https://cloud.google.com/vertex-ai/generative-ai/docs
  findings: |
    Vertex AI integration patterns for Google ADK.
    Model deployment and management.
    Authentication and security best practices.
```

### Cross-Platform Integration Research

```yaml
# CROSS-PLATFORM PATTERNS - Synthesis from A2A and ADK research
integration_patterns:
  - A2A server hosting Google ADK agents
  - Cross-platform task delegation from/to Google ADK agents  
  - Agent discovery and capability advertisement
  - Secure communication channels between different platforms
  - Unified monitoring for multi-platform agent networks

deployment_patterns:
  - Cloud Run deployment of A2A-compatible Google ADK agents
  - Google Cloud infrastructure for A2A agent networks
  - Scaling patterns for distributed A2A agent systems
  - Cost optimization for cross-platform agent coordination
```

### Current Template Structure (ANALYZED)

```bash
# Base template patterns to extend from template-generator analysis
template-generator/
├── PRPs/templates/prp_template_base.md  # Base template structure to specialize
├── .claude/commands/                    # Command patterns to adapt for A2A-ADK
├── copy_template.py                     # Template deployment pattern to replicate
└── examples/                           # Example patterns to adapt for A2A-ADK

# Google ADK reference patterns from existing use case
google-adk/
├── CLAUDE.md                           # Google ADK-specific patterns to extend
├── examples/                           # Google ADK examples to make A2A-compatible
└── PRPs/templates/                     # Google ADK PRP patterns to merge with A2A
```

### A2A-Google ADK Architecture Requirements

```typescript
// A2A-compatible Google ADK agent architecture
interface A2AGooogleADKAgent {
  // A2A Protocol compliance
  a2a_server: {
    agent_registration: string[];
    capability_advertisement: string[];
    cross_platform_communication: string[];
    task_delegation_patterns: string[];
  };
  
  // Google ADK integration
  google_adk: {
    vertex_ai_models: string[];
    tool_integration: string[];
    workflow_orchestration: string[];
    cloud_deployment: string[];
  };
  
  // Cross-platform coordination
  interoperability: {
    protocol_compliance: string[];
    security_patterns: string[];
    monitoring_integration: string[];
    testing_frameworks: string[];
  };
}
```

### Template Generation Patterns (ESTABLISHED)

```typescript
// CRITICAL: A2A-Google ADK template must follow these patterns

// 1. ALWAYS inherit from base context engineering AND A2A protocol compliance
const basePatterns = {
  context_engineering: "INITIAL.md → generate-prp → execute-prp workflow",
  a2a_compliance: "A2A server setup → agent registration → cross-platform communication",
  google_integration: "Vertex AI models → ADK tools → Cloud deployment"
};

// 2. ALWAYS specialize for A2A protocol AND Google ADK together
const specialization = {
  a2a_patterns: "Replace generic agents with A2A-compatible implementations",
  google_cloud: "Include Vertex AI, Cloud Run, and Google Cloud patterns", 
  cross_platform: "Enable communication with LangGraph, CrewAI, etc.",
  security: "Implement A2A security patterns with Google Cloud IAM"
};

// 3. ALWAYS maintain production readiness
const quality_gates = {
  a2a_compliance: "All agents must be A2A protocol compliant",
  google_integration: "Native Google Cloud deployment patterns",
  cross_platform_testing: "Validation with multiple agent platforms",
  production_ready: "Enterprise-grade security and monitoring"
};
```

## Implementation Blueprint

### Phase 1: A2A Protocol Analysis and Pattern Extraction

```yaml
Task 1 - A2A Protocol Implementation Analysis:
  ANALYZE A2A protocol requirements for Google ADK integration:
    - A2A server setup patterns with Google ADK agents
    - Agent registration and capability advertisement mechanisms
    - Cross-platform communication protocols and message formats
    - Task delegation patterns between A2A-compatible agents
    - Security and authentication requirements for A2A networks

Task 2 - Google ADK-A2A Integration Planning:
  PLAN how to make Google ADK agents A2A-compatible:
    - Vertex AI model integration within A2A framework
    - Google ADK tool registration in A2A agent capabilities
    - Workflow orchestration patterns for A2A-compatible agents
    - Cloud deployment patterns for A2A agent networks
    - Authentication bridge between Google Cloud and A2A protocol
```

### Phase 2: Template Package Structure Creation

```yaml
Task 3 - Create A2A-Google ADK Template Directory:
  CREATE complete use case directory structure:
    - use-cases/a2a-google-adk/ with all required subdirectories
    - .claude/commands/ for A2A-ADK specific PRP commands
    - PRPs/templates/ for A2A-ADK specialized PRP template
    - examples/ for A2A-compatible Google ADK agent examples
    - config/ for A2A server and Google Cloud configuration

Task 4 - Generate A2A-Google ADK CLAUDE.md:
  CREATE specialized global rules file:
    - A2A protocol compliance requirements and validation
    - Google ADK integration patterns within A2A framework
    - Cross-platform agent communication and coordination patterns
    - Google Cloud deployment and scaling for A2A agent networks
    - Security best practices for A2A-compatible Google ADK agents
    - Development workflow for A2A protocol compliance testing
```

### Phase 3: A2A-Specific PRP Command Generation

```yaml
Task 5 - Create A2A-Google ADK PRP Commands:
  GENERATE domain-specific slash commands:
    - generate-a2a-google-adk-prp.md with A2A protocol research patterns
    - execute-a2a-google-adk-prp.md with A2A compliance validation loops
    - Commands include A2A server setup and cross-platform testing
    - Integration with Google Cloud deployment and monitoring patterns

Task 6 - Develop A2A-Google ADK Base PRP Template:
  CREATE specialized prp_a2a_google_adk_base.md:
    - Pre-filled with A2A protocol context and Google ADK patterns
    - A2A compliance success criteria and validation gates
    - Cross-platform agent coordination requirements
    - Google Cloud integration and deployment validation loops
    - Security and authentication pattern requirements
```

### Phase 4: Example Implementation and Documentation

```yaml
Task 7 - Create A2A-Compatible Google ADK Examples:
  GENERATE comprehensive working examples:
    - basic_a2a_agent/ - Simple A2A-compatible Google ADK agent
    - a2a_server_setup/ - Complete A2A server configuration
    - cross_platform_delegation/ - Task delegation between platforms
    - multi_agent_coordination/ - A2A agent network coordination
    - google_cloud_deployment/ - Cloud Run deployment for A2A agents
    - a2a_testing_framework/ - A2A compliance testing and validation

Task 8 - Create Configuration Templates:
  GENERATE A2A and Google Cloud configuration:
    - a2a_server_config.py for A2A server setup
    - google_cloud_config.py for Vertex AI and Cloud Run integration
    - agent_registry.py for agent discovery and registration
    - Environment configuration templates for A2A networks

Task 9 - Generate AI Documentation:
  CREATE specialized A2A-Google ADK documentation:
    - a2a_protocol_patterns.md - A2A implementation patterns
    - google_adk_integration.md - Google ADK with A2A integration
    - cross_platform_agent_coordination.md - Multi-platform patterns
    - Include gotchas, security considerations, and troubleshooting
```

### Phase 5: Template Deployment and Validation

```yaml
Task 10 - Create Template Copy Script:
  CREATE Python deployment script:
    - copy_template.py accepting target directory argument
    - Copies entire A2A-Google ADK template structure
    - Includes all files: CLAUDE.md, commands, PRPs, examples, config
    - Error handling and success feedback with next steps
    - Usage: python copy_template.py /path/to/new-a2a-project

Task 11 - Generate Comprehensive README:
  CREATE comprehensive A2A-Google ADK README.md:
    - A2A protocol overview and Google ADK integration benefits
    - Template copy script usage (prominently featured)
    - PRP framework workflow for A2A-compatible agents
    - Quick start guide with A2A server setup
    - Cross-platform agent coordination examples
    - Google Cloud deployment patterns and best practices
    - A2A compliance testing and validation procedures
```

## Validation Loop

### Level 1: Template Structure Validation

```bash
# CRITICAL: Verify complete A2A-Google ADK template structure
find use-cases/a2a-google-adk -type f | sort
ls -la use-cases/a2a-google-adk/.claude/commands/
ls -la use-cases/a2a-google-adk/PRPs/templates/
ls -la use-cases/a2a-google-adk/examples/
ls -la use-cases/a2a-google-adk/config/

# Verify copy script exists and functions
test -f use-cases/a2a-google-adk/copy_template.py
python use-cases/a2a-google-adk/copy_template.py --help

# Expected: All required A2A-Google ADK files present
# If missing: Generate missing components following A2A patterns
```

### Level 2: A2A Protocol Compliance Validation

```bash
# Verify A2A protocol compliance in templates
grep -r "a2a-sdk\|A2AServer\|agent.*registration" use-cases/a2a-google-adk/
grep -r "cross.*platform\|inter.*agent" use-cases/a2a-google-adk/
grep -r "task.*delegation\|agent.*discovery" use-cases/a2a-google-adk/

# Check for Google ADK integration patterns
grep -r "vertex.*ai\|google.*adk\|gemini" use-cases/a2a-google-adk/
grep -r "cloud.*run\|google.*cloud" use-cases/a2a-google-adk/

# Expected: A2A protocol patterns and Google ADK integration present
# If missing: Add A2A compliance patterns and Google integration
```

### Level 3: Example and Configuration Validation

```bash
# Test A2A-compatible examples
cd use-cases/a2a-google-adk/examples/basic_a2a_agent
python -m py_compile *.py  # Check Python syntax

# Test configuration templates
cd ../config/
python -c "import a2a_server_config, google_cloud_config, agent_registry"

# Test A2A server setup example
cd ../examples/a2a_server_setup/
python -m py_compile *.py

# Expected: All Python examples compile without errors
# If failing: Fix syntax and import errors in examples
```

### Level 4: PRP Framework Integration Testing

```bash
# Verify PRP framework integration
cd use-cases/a2a-google-adk/

# Test A2A-specific PRP generation
/generate-a2a-google-adk-prp INITIAL.md
ls PRPs/*.md | grep -v templates

# Test template completeness
grep -r "A2A.*protocol" . | wc -l  # Should have A2A patterns
grep -r "Google.*ADK\|Vertex.*AI" . | wc -l  # Should have Google integration
grep -r "cross.*platform" . | wc -l  # Should have interoperability

# Expected: A2A-Google ADK PRP generation works, content specialized
# If failing: Debug A2A-specific command patterns and templates
```

## Final Validation Checklist

### A2A Protocol Integration

- [ ] A2A server setup patterns documented and working
- [ ] Agent registration and discovery mechanisms implemented
- [ ] Cross-platform communication examples included
- [ ] Task delegation patterns between A2A agents working
- [ ] A2A protocol compliance validation included
- [ ] Security patterns for A2A networks documented

### Google ADK Integration

- [ ] Vertex AI model integration within A2A framework
- [ ] Google ADK tool registration in A2A capabilities
- [ ] Cloud Run deployment patterns for A2A agents
- [ ] Google Cloud authentication with A2A protocol
- [ ] ADK workflow orchestration in A2A context
- [ ] Google Cloud monitoring for A2A agent networks

### Template Package Quality

- [ ] Complete directory structure: `tree use-cases/a2a-google-adk`
- [ ] Copy script functional: `python copy_template.py --help`
- [ ] No placeholder content: `grep -r "TODO\|PLACEHOLDER"`
- [ ] Working examples: All Python files compile successfully
- [ ] README comprehensive: A2A protocol and Google ADK integration
- [ ] PRP commands functional: A2A-specific PRP generation works

### Production Readiness

- [ ] Security patterns: A2A network security and Google Cloud IAM
- [ ] Monitoring integration: A2A agent network observability
- [ ] Testing framework: A2A compliance validation tools
- [ ] Documentation complete: All patterns and gotchas documented
- [ ] Enterprise patterns: Production deployment and scaling
- [ ] Cross-platform compatibility: Tested with multiple agent platforms

---

## Anti-Patterns to Avoid

### A2A Protocol Implementation

- ❌ Don't create A2A-incompatible agents - always follow A2A protocol specifications
- ❌ Don't ignore cross-platform compatibility - test with multiple agent frameworks
- ❌ Don't skip agent registration - always implement proper A2A discovery mechanisms
- ❌ Don't forget security - implement A2A authentication and trust patterns

### Google ADK Integration

- ❌ Don't bypass Google Cloud patterns - use native Vertex AI and Cloud Run integration
- ❌ Don't ignore cost optimization - implement Google Cloud cost controls
- ❌ Don't skip authentication - properly integrate Google Cloud IAM with A2A security
- ❌ Don't forget monitoring - include Google Cloud observability for A2A networks

### Template Quality

- ❌ Don't create generic content - specialize deeply for A2A-Google ADK patterns
- ❌ Don't skip working examples - all examples must be A2A-compliant and functional
- ❌ Don't ignore validation - include comprehensive A2A compliance testing
- ❌ Don't forget documentation - document all A2A patterns and Google integration gotchas