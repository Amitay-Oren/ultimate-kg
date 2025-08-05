---
name: "A2A-Compatible Google ADK Agent Development"
description: "Base PRP template for building A2A-compatible AI agents using Google Agent Development Kit with cross-platform interoperability"
---

## Purpose

Build A2A (Agent-to-Agent) protocol compatible AI agents using Google's Agent Development Kit that can seamlessly communicate and collaborate with agents from different platforms (LangGraph, CrewAI, Semantic Kernel, etc.) while leveraging Google Cloud infrastructure.

## Core Principles

1. **A2A Protocol Compliance**: Full adherence to Agent-to-Agent protocol specifications
2. **Cross-Platform Interoperability**: Enable seamless communication with agents from any platform
3. **Google Cloud Integration**: Leverage Vertex AI, Cloud Run, and Google Cloud services
4. **Production-Ready Architecture**: Enterprise-grade patterns for deployment and scaling
5. **Security-First Design**: Comprehensive security for inter-agent communication

---

## Goal

**What to build:** [SPECIFIC_A2A_GOOGLE_ADK_FEATURE]

Build a production-ready A2A-compatible Google ADK agent that:
- Implements A2A protocol for cross-platform agent communication
- Integrates Google ADK capabilities (Vertex AI models, tools, workflows)
- Enables task delegation to/from agents on other platforms
- Deploys on Google Cloud infrastructure with proper monitoring
- Maintains security and performance in multi-agent networks

## Why

**Business/Technical Justification:**
- **Cross-Platform Collaboration**: Enable Google ADK agents to work with any agent ecosystem
- **Scalable Architecture**: Build distributed agent systems across multiple platforms
- **Cost Optimization**: Leverage best capabilities from each agent platform
- **Future-Proofing**: Use open standards for agent interoperability
- **Enterprise Integration**: Connect with existing agent infrastructure

## What

### A2A-Google ADK Implementation Requirements

**A2A Protocol Integration:**
- A2A server setup hosting Google ADK agents
- Agent registration and capability advertisement
- Cross-platform agent discovery and communication
- Task delegation protocols between different agent platforms
- A2A compliance validation and testing

**Google ADK Features:**
- Vertex AI model integration (Gemini, PaLM) within A2A framework
- Google ADK tool ecosystem exposed through A2A capabilities
- Workflow orchestration (Sequential, Parallel, Loop) with A2A compatibility
- Google Cloud authentication integrated with A2A security
- Cloud deployment patterns for A2A agent networks

**Cross-Platform Coordination:**
- Agent communication with LangGraph, CrewAI, Semantic Kernel agents
- Multi-agent workflow orchestration using A2A protocol
- Task result aggregation from multiple agent platforms
- Error handling and resilience in cross-platform scenarios
- Performance optimization for A2A protocol overhead

### Success Criteria

- [ ] A2A server successfully hosts Google ADK agents
- [ ] Cross-platform agent communication working correctly
- [ ] Agent discovery and registration mechanisms operational
- [ ] Task delegation between platforms functioning
- [ ] Google Cloud integration properly configured
- [ ] A2A protocol compliance validated
- [ ] Security patterns implemented for agent networks
- [ ] Monitoring and observability systems operational
- [ ] Performance meets requirements for production use
- [ ] Documentation complete for deployment and maintenance

## All Needed Context

### A2A Protocol Documentation

```yaml
# A2A PROTOCOL FOUNDATION
- url: https://a2a-protocol.org/latest/
  why: Core A2A protocol specifications and architecture patterns
  
- url: https://a2a-protocol.org/latest/tutorials/python
  why: Python implementation patterns for A2A protocol

- url: https://github.com/a2aproject/a2a-python
  why: A2A Python SDK documentation and installation procedures

- url: https://github.com/a2aproject/a2a-samples/tree/main/samples/python
  why: A2A Python sample implementations and patterns
```

### Google ADK Integration

```yaml
# GOOGLE ADK FOUNDATION
- url: https://google.github.io/adk-docs/
  why: Official Google ADK documentation and capabilities

- url: https://cloud.google.com/vertex-ai/generative-ai/docs
  why: Vertex AI integration patterns for Google ADK agents

- url: https://cloud.google.com/run/docs
  why: Cloud Run deployment patterns for A2A agent servers

- file: ../../../google-adk/examples/
  why: Working Google ADK agent implementation patterns
```

### Cross-Platform Integration Research

```yaml
# CROSS-PLATFORM PATTERNS
research_areas:
  - A2A server architecture with Google ADK agents
  - Cross-platform task delegation and coordination patterns  
  - Agent discovery and capability advertisement mechanisms
  - Security patterns for A2A network communication
  - Performance optimization for cross-platform agent coordination
  - Monitoring and observability for distributed agent networks
```

### Current Implementation Context

```bash
# Project structure context
use-cases/a2a-google-adk/
├── CLAUDE.md                    # A2A-Google ADK development patterns
├── config/                      # A2A server and Google Cloud configuration
├── examples/                    # A2A-compatible Google ADK examples
└── PRPs/                       # A2A-Google ADK specialized PRPs
```

### A2A-Google ADK Architecture Requirements

```typescript
// A2A-compatible Google ADK agent architecture
interface A2AGooogleADKImplementation {
  // A2A Protocol compliance
  a2a_server: {
    agent_registration: AgentRegistration[];
    capability_advertisement: AgentCapabilities[];
    cross_platform_communication: CommunicationProtocol[];
    task_delegation: TaskDelegationPattern[];
  };
  
  // Google ADK integration
  google_adk: {
    vertex_ai_models: VertexAIModel[];
    tool_integration: GoogleADKTool[];
    workflow_orchestration: WorkflowPattern[];
    cloud_deployment: CloudDeploymentPattern[];
  };
  
  // Cross-platform features
  interoperability: {
    platform_adapters: PlatformAdapter[];
    protocol_translation: ProtocolTranslator[];
    security_integration: SecurityPattern[];
    monitoring_integration: MonitoringPattern[];
  };
}
```

## Implementation Blueprint

### Phase 1: A2A Protocol Setup

```yaml
Task 1 - A2A Server Configuration:
  IMPLEMENT A2A server to host Google ADK agents:
    - Install a2a-sdk with gRPC and telemetry support
    - Configure A2A server for Google Cloud deployment
    - Set up agent registration and discovery mechanisms
    - Implement A2A protocol compliance validation
    - Configure security and authentication for A2A networks

Task 2 - Google ADK Agent A2A Integration:
  MAKE Google ADK agents A2A-compatible:
    - Wrap Google ADK agents with A2A protocol interfaces
    - Register agent capabilities in A2A discovery system
    - Implement A2A message handling for Google ADK agents
    - Configure Vertex AI model access through A2A requests
    - Set up Google ADK tool exposure via A2A capabilities
```

### Phase 2: Cross-Platform Communication

```yaml
Task 3 - Cross-Platform Agent Discovery:
  IMPLEMENT agent discovery across platforms:
    - Configure A2A agent discovery for LangGraph agents
    - Set up communication with CrewAI agents via A2A protocol
    - Implement Semantic Kernel agent integration patterns
    - Create agent capability matching and selection logic
    - Set up fallback and error handling for agent unavailability

Task 4 - Task Delegation Implementation:
  BUILD cross-platform task delegation:
    - Implement task routing to appropriate platform agents
    - Create result aggregation from multiple agent platforms
    - Set up task status tracking across platforms
    - Implement error handling and retry mechanisms
    - Create performance monitoring for cross-platform tasks
```

### Phase 3: Google Cloud Integration

```yaml
Task 5 - Google Cloud Deployment:
  DEPLOY A2A agents to Google Cloud:
    - Configure Cloud Run deployment for A2A server
    - Set up Google Cloud authentication for A2A agents
    - Implement Vertex AI integration within A2A framework
    - Configure auto-scaling for A2A agent networks
    - Set up Google Cloud monitoring and logging

Task 6 - Security and Performance Optimization:
  OPTIMIZE A2A agent networks for production:
    - Implement A2A network security with Google Cloud IAM
    - Set up TLS encryption for cross-platform communication
    - Optimize A2A protocol performance and reduce latency
    - Implement cost controls for Google Cloud resources
    - Set up disaster recovery and failover mechanisms
```

## Validation Loop

### Level 1: A2A Protocol Compliance

```bash
# Test A2A server functionality
curl -X GET http://localhost:8080/health
curl -X GET http://localhost:8080/agents
python config/a2a_server_config.py --validate

# Validate A2A protocol compliance
a2a-validator --server-url http://localhost:8080
a2a-validator --agent-url http://localhost:8080/agents/google-adk-agent

# Expected: A2A server operational, agents properly registered
# If failing: Check A2A server configuration and agent registration
```

### Level 2: Cross-Platform Communication Testing

```bash
# Test cross-platform agent communication
python examples/cross_platform_delegation/test_langraph_communication.py
python examples/cross_platform_delegation/test_crewai_integration.py
python examples/cross_platform_delegation/test_semantic_kernel_delegation.py

# Test multi-agent coordination
python examples/multi_agent_coordination/test_cross_platform_workflow.py

# Expected: Successful communication with agents from different platforms
# If failing: Check platform adapters and protocol translation
```

### Level 3: Google Cloud Integration Validation

```bash
# Test Google Cloud authentication and Vertex AI
gcloud auth application-default print-access-token
python -c "from google.cloud import aiplatform; aiplatform.init()"

# Test Cloud Run deployment
gcloud run deploy a2a-test --source . --region us-central1 --no-traffic
gcloud run services describe a2a-test --region us-central1

# Test Google ADK integration within A2A
python tests/google_integration/test_vertex_ai_a2a_compatibility.py

# Expected: Google Cloud services accessible through A2A agents
# If failing: Check Google Cloud authentication and service configuration
```

### Level 4: Performance and Production Readiness

```bash
# Performance testing
python tests/performance/test_a2a_protocol_overhead.py
python tests/performance/test_cross_platform_latency.py
python tests/performance/benchmark_agent_coordination.py

# Load testing
python tests/load/test_concurrent_cross_platform_requests.py

# Security testing
python tests/security/test_a2a_network_security.py
python tests/security/test_cross_platform_authentication.py

# Expected: Performance meets production requirements
# If failing: Optimize A2A protocol handling and resource allocation
```

## Final Validation Checklist

### A2A Protocol Implementation
- [ ] A2A server hosting Google ADK agents successfully
- [ ] Agent registration and discovery working correctly
- [ ] Cross-platform agent communication functional
- [ ] Task delegation between platforms operational
- [ ] A2A protocol compliance validated
- [ ] Error handling and resilience patterns implemented

### Google Cloud Integration
- [ ] Vertex AI models accessible through A2A agents
- [ ] Google ADK tools exposed via A2A capabilities
- [ ] Cloud Run deployment successful and scalable
- [ ] Google Cloud authentication integrated with A2A security
- [ ] Monitoring and logging operational for A2A networks
- [ ] Cost controls and optimization implemented

### Production Readiness
- [ ] Security patterns protecting A2A network communication
- [ ] Performance optimization minimizing protocol overhead
- [ ] Load testing confirms scalability requirements
- [ ] Documentation complete for deployment and maintenance
- [ ] Disaster recovery and failover mechanisms tested
- [ ] Compliance with enterprise security requirements

---

## Anti-Patterns to Avoid

### A2A Protocol Implementation
- ❌ Don't create A2A-incompatible agents - always follow protocol specifications
- ❌ Don't ignore cross-platform testing - validate with multiple agent frameworks
- ❌ Don't skip agent registration - implement proper discovery mechanisms
- ❌ Don't forget error handling - plan for cross-platform communication failures

### Google Cloud Integration
- ❌ Don't bypass Google Cloud best practices - use native patterns
- ❌ Don't ignore cost optimization - implement proper resource controls
- ❌ Don't skip authentication - properly integrate Google Cloud IAM
- ❌ Don't forget monitoring - implement comprehensive observability

### Production Deployment
- ❌ Don't deploy without testing - validate all cross-platform scenarios
- ❌ Don't ignore security - implement comprehensive network protection
- ❌ Don't skip performance optimization - minimize A2A protocol overhead
- ❌ Don't forget documentation - document all integration patterns and gotchas