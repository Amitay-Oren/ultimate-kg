# Generate Google ADK Agent PRP

## Feature file: $ARGUMENTS

Generate a comprehensive PRP for building AI agents and multi-agent systems using Google's Agent Development Kit based on the detailed requirements in the INITIAL.md file. This follows the standard PRP framework workflow: INITIAL.md → generate-google-adk-prp → execute-google-adk-prp.

**CRITICAL: Web search and Google ADK documentation research is your best friend. Use it extensively throughout this process.**

## Research Process

1. **Read and Understand Agent Requirements**
   - Read the specified INITIAL.md file thoroughly
   - Understand the target agent functionality and multi-agent coordination needs
   - Note any specific tools, integrations, or Google Cloud services mentioned
   - Identify the scope and complexity of the agent system needed

2. **Extensive Google ADK Research (CRITICAL)**
   - **Web search Google Agent Development Kit extensively** - this is essential
   - Study official documentation at google.github.io/adk-docs
   - Research agent architecture patterns and multi-agent coordination
   - Find real-world ADK implementation examples and tutorials
   - Identify common gotchas, pitfalls, and Google Cloud integration issues
   - Look for established agent project structure conventions

3. **Agent Pattern Analysis**
   - Examine successful ADK implementations found through web research
   - Identify agent architecture and multi-agent coordination patterns
   - Extract reusable agent code patterns and configuration templates
   - Document ADK-specific development workflows and deployment patterns
   - Note testing frameworks and agent validation approaches

4. **Google Cloud Integration Research**
   - Research Vertex AI integration patterns for model access
   - Study Cloud Run deployment patterns for agent applications
   - Investigate service account and IAM configuration for production
   - Document cost optimization strategies for agent deployments
   - Research monitoring and logging patterns for agent operations

## PRP Generation

Using PRPs/templates/prp_google_adk_base.md as the foundation:

### Critical Context to Include from Web Research

**Google ADK Documentation (from web search)**:
- Official Google ADK documentation URLs with specific agent examples
- Getting started guides and agent creation tutorials
- Multi-agent coordination and workflow documentation
- Google Cloud integration guides and best practices

**Agent Implementation Patterns (from research)**:
- ADK-specific agent project structures and conventions
- Agent configuration management approaches
- Multi-agent coordination and delegation patterns
- Tool integration and custom tool creation approaches

**Real-World Agent Examples**:
- Links to successful ADK agent implementations found online
- Agent code snippets and configuration examples
- Common multi-agent integration patterns
- Google Cloud deployment and setup procedures

### Implementation Blueprint

Based on web research findings:
- **Agent Architecture Analysis**: Document ADK agent characteristics and coordination patterns
- **Multi-Agent Design**: Plan complex agent system components and interactions
- **Google Cloud Integration**: How to integrate with Vertex AI, Cloud Run, and other services
- **Validation Design**: ADK-appropriate agent testing and validation loops

### Validation Gates (Must be Executable)

```bash
# Agent Implementation Validation
ls -la agents/ tools/ configs/
find . -name "*.py" -exec python -m py_compile {} \;  # Python syntax check

# Google ADK Import Testing
python -c "from google.adk.agents import Agent, LlmAgent; print('ADK imports successful')"

# Agent Configuration Validation
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Environment loaded')"

# Google Cloud Integration Testing
gcloud auth application-default print-access-token > /dev/null 2>&1 && echo "GCloud auth configured" || echo "GCloud auth needs setup"
```

*** CRITICAL: Do extensive web research on Google ADK before writing the PRP ***
*** Use WebSearch tool extensively to understand Google ADK agents deeply ***

## Output

Save as: `PRPs/agent-{agent-name}.md`

## Quality Checklist

- [ ] Extensive web research completed on Google Agent Development Kit
- [ ] Official Google ADK documentation thoroughly reviewed
- [ ] Real-world agent examples and patterns identified
- [ ] Complete agent system architecture planned
- [ ] Multi-agent coordination patterns designed
- [ ] Google Cloud integration strategy developed
- [ ] Agent-specific validation designed
- [ ] All web research findings documented in PRP
- [ ] ADK-specific gotchas and patterns captured
- [ ] Tool integration and custom tool patterns included
- [ ] Deployment and monitoring strategies planned

Score the PRP on a scale of 1-10 (confidence level for creating comprehensive, immediately usable Google ADK agents based on thorough research).

Remember: The goal is creating complete, sophisticated agent systems that leverage Google ADK's multi-agent capabilities and Google Cloud integration through comprehensive research and documentation.