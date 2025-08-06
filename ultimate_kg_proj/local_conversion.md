# Local Conversion Plan: Agentic GraphRAG System

## Overview
Convert the Agentic GraphRAG system from Google Cloud dependency to fully local operation using Google ADK with Gemini API, based on the successful `kg_broker_agent` pattern found in `context/google-adk/examples/kg_broker_agent/`.

## Current State Analysis
- **Problem**: Hard dependencies on `google.cloud.aiplatform` and Vertex AI authentication
- **Solution**: Use direct Gemini API calls like the working `kg_broker_agent` example
- **Target**: 100% local operation with only Gemini API key requirement

## Conversion Strategy
1. **Remove Google Cloud authentication** - Replace with direct Gemini API usage
2. **Update configuration system** - Make Google Cloud optional, add Gemini API config  
3. **Simplify agent initialization** - Follow proven `kg_broker_agent` pattern
4. **Update dependencies** - Remove cloud-specific packages
5. **Create comprehensive verification** - Test suite to ensure 100% local operation

---

## Phase 1: Analysis & Preparation (30 minutes)

### 1.1 Document Current Dependencies
- [ ] List all files with Google Cloud imports
  - [ ] `agentic_graphrag/server/a2a_server.py` - Lines 16-17
  - [ ] `agentic_graphrag/agents/kg_agent.py` - Lines 14-18
  - [ ] `agentic_graphrag/agents/extraction_pipeline.py` - Lines 14-15
  - [ ] `agentic_graphrag/agents/connection_detector.py` - Line 15
  - [ ] `agentic_graphrag/config/__init__.py` - Configuration validation
  - [ ] `agentic_graphrag/requirements.txt` - Package dependencies

### 1.2 Create Backup & Environment
- [ ] Create backup branch: `git checkout -b backup-before-local-conversion`
- [ ] Create feature branch: `git checkout -b convert-to-local-mode`
- [ ] Verify current system runs with Google Cloud (baseline test)
- [ ] Document current `.env` configuration

### 1.3 Set Up Testing Environment
- [ ] Obtain Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- [ ] Create test `.env` file with Gemini API key only
- [ ] Verify local Neo4j is running: `docker ps | grep neo4j`
- [ ] Verify MCP server can start independently

---

## Phase 2: Configuration Updates (30 minutes)

### 2.1 Update Configuration Classes (`config/__init__.py`)
- [ ] Make `GoogleCloudConfig.project_id` optional (remove required validation)
- [ ] Add `gemini_api_key` field to configuration
- [ ] Update `validate_config()` method:
  - [ ] Remove `GOOGLE_CLOUD_PROJECT` requirement
  - [ ] Add `GEMINI_API_KEY` validation
  - [ ] Make Google Cloud fields optional
- [ ] Add local mode detection logic

### 2.2 Update Environment Configuration (`.env.example`)
- [ ] Add Gemini API configuration section:
  ```env
  # Gemini API Configuration (for local mode)
  GEMINI_API_KEY=your_gemini_api_key_here
  ADK_MODEL=gemini-2.0-flash
  ```
- [ ] Mark Google Cloud variables as optional:
  ```env
  # Google Cloud Configuration (OPTIONAL - for cloud deployment only)
  # GOOGLE_CLOUD_PROJECT=your-project-id
  # VERTEX_AI_LOCATION=us-central1  
  # GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
  ```
- [ ] Add local mode instructions in comments

### 2.3 Add Local Mode Configuration
- [ ] Add `local_mode` detection in `SystemConfig.__init__()`
- [ ] Create configuration validation specifically for local mode
- [ ] Add helper method `is_local_mode()` to determine operation mode

---

## Phase 3: Remove Google Cloud Dependencies (45 minutes)

### 3.1 Update A2A Server (`server/a2a_server.py`)
- [ ] Remove imports:
  - [ ] `from google.cloud import aiplatform`
  - [ ] `from google.auth import default`
- [ ] Update `_initialize_google_cloud()` method:
  - [ ] Make method optional/conditional
  - [ ] Skip initialization if in local mode
  - [ ] Add local mode logging
- [ ] Update initialization flow in `initialize()`:
  - [ ] Add conditional Google Cloud initialization
  - [ ] Ensure system works without Google Cloud
- [ ] Update status reporting to reflect local vs cloud mode

### 3.2 Update KG Agent (`agents/kg_agent.py`)
- [ ] Replace Google ADK imports with local pattern:
  ```python
  # Remove these imports
  # from google.adk.agents.llm_agent import LlmAgent
  # from google.adk.runners import Runner
  # from google.adk.sessions import InMemorySessionService
  # from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams
  # from google.genai import types
  
  # Add these imports (following kg_broker_agent pattern)
  from google.genai import types
  from google.adk.agents.llm_agent import LlmAgent
  from google.adk.runners import Runner
  from google.adk.sessions import InMemorySessionService
  from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams
  ```
- [ ] Update agent initialization to match `kg_broker_agent` pattern:
  - [ ] Use direct model name (e.g., `gemini-2.0-flash`)
  - [ ] Remove Vertex AI configuration
  - [ ] Use local MCP connection parameters
- [ ] Test agent creation without Google Cloud authentication

### 3.3 Update Extraction Pipeline (`agents/extraction_pipeline.py`)
- [ ] Remove Google ADK cloud-specific imports
- [ ] Replace with local agent pattern
- [ ] Update agent coordination to use local models only
- [ ] Ensure pipeline works with direct API calls

### 3.4 Update Connection Detector (`agents/connection_detector.py`)
- [ ] Remove Google ADK cloud imports
- [ ] Update to use local LLM agent pattern
- [ ] Ensure vector similarity works with local embeddings
- [ ] Test connection detection without cloud dependencies

### 3.5 Update Dependencies (`requirements.txt`)
- [ ] Remove cloud-specific packages:
  - [ ] `google-cloud-aiplatform>=1.70.0` (remove)
  - [ ] Keep `google-adk>=1.0.0` (works locally)
- [ ] Add any missing local dependencies:
  - [ ] Ensure `python-dotenv` is included
  - [ ] Verify all Google ADK local dependencies

---

## Phase 4: Implement Local Agent Pattern (45 minutes)

### 4.1 Create Local LLM Client (`agents/local_llm_client.py`)
- [ ] Create wrapper class for direct Gemini API usage
- [ ] Implement error handling and retry logic
- [ ] Add logging for API calls
- [ ] Follow `kg_broker_agent` authentication pattern

### 4.2 Update Agent Initialization Pattern
- [ ] Update `KnowledgeGraphAgent` class in `agents/kg_agent.py`:
  - [ ] Follow exact pattern from `kg_broker_agent/agent.py`
  - [ ] Use `LlmAgent` with direct model specification
  - [ ] Configure MCP toolset with local connection
  - [ ] Remove all Vertex AI references
- [ ] Test agent creation and basic functionality

### 4.3 Update Agent Coordination
- [ ] Ensure all sub-agents use local model specification
- [ ] Update multi-agent communication to work without cloud
- [ ] Test agent-to-agent communication locally
- [ ] Verify MCP tool integration still functions

### 4.4 Update Main System Integration (`main.py`)
- [ ] Update logging configuration (remove cloud-specific log levels)
- [ ] Ensure system startup works without Google Cloud
- [ ] Update status reporting for local mode
- [ ] Test complete system initialization

---

## Phase 5: Testing & Verification (30 minutes) 

### 5.1 Create Local Mode Tests (`tests/test_local_mode.py`)
- [ ] Test system startup without Google Cloud credentials
- [ ] Test agent initialization with Gemini API only
- [ ] Test MCP integration in local mode
- [ ] Test complete data processing workflow
- [ ] Test error handling for missing Gemini API key

### 5.2 Environment Isolation Testing
- [ ] Create clean test environment:
  ```bash
  # Remove all Google Cloud environment variables
  unset GOOGLE_CLOUD_PROJECT
  unset VERTEX_AI_LOCATION  
  unset GOOGLE_APPLICATION_CREDENTIALS
  
  # Set only required local variables
  export GEMINI_API_KEY=your_key_here
  export LLM_API_KEY=your_llm_key_here
  ```
- [ ] Test system startup in clean environment
- [ ] Verify no Google Cloud calls are made

### 5.3 Functional Testing
- [ ] Test knowledge ingestion workflow:
  ```bash
  curl -X POST http://localhost:8080/agents/kg_ingest \
    -H "Content-Type: application/json" \
    -d '{"data": "Test data for local processing"}'
  ```
- [ ] Test knowledge search functionality
- [ ] Test system status endpoint
- [ ] Verify all features work without cloud dependencies

### 5.4 Import and Dependency Verification
- [ ] Run import test:
  ```python
  python -c "
  import sys
  import agentic_graphrag
  google_modules = [m for m in sys.modules if 'google.cloud' in m]
  assert len(google_modules) == 0, f'Found Google Cloud imports: {google_modules}'
  print('✅ No Google Cloud imports found')
  "
  ```
- [ ] Run dependency scan: `pip list | grep google`
- [ ] Verify only local Google packages remain

---

## Phase 6: Documentation & Cleanup (15 minutes)

### 6.1 Update Documentation
- [ ] Update main `README.md`:
  - [ ] Add local setup section
  - [ ] Document Gemini API key requirement
  - [ ] Remove Google Cloud setup instructions
  - [ ] Add troubleshooting for local mode
- [ ] Update `agentic_graphrag/README.md`:
  - [ ] Emphasize local-first operation
  - [ ] Update configuration examples
  - [ ] Add local testing instructions

### 6.2 Create Local Setup Guide
- [ ] Document Gemini API key setup process
- [ ] Create step-by-step local installation guide
- [ ] Add common troubleshooting scenarios
- [ ] Document differences between local and cloud modes

### 6.3 Cleanup and Validation
- [ ] Remove any unused Google Cloud configuration files
- [ ] Clean up commented-out cloud code
- [ ] Run final system test
- [ ] Create verification checklist for users

---

## Success Criteria Checklist

### ✅ Environment Independence
- [ ] System starts successfully without `GOOGLE_CLOUD_PROJECT` environment variable
- [ ] System starts successfully without `GOOGLE_APPLICATION_CREDENTIALS` environment variable  
- [ ] System starts successfully without any Google Cloud authentication
- [ ] System works with only `GEMINI_API_KEY` environment variable

### ✅ Functionality Verification
- [ ] Knowledge ingestion works (`/agents/kg_ingest` endpoint)
- [ ] Knowledge search works (`/agents/kg_search` endpoint)
- [ ] System status works (`/agents/kg_status` endpoint)
- [ ] MCP integration with Cognee works
- [ ] Agent coordination and communication works
- [ ] Notification system works

### ✅ Technical Verification
- [ ] No Google Cloud imports in any Python files
- [ ] No calls to Google Cloud APIs (aiplatform, auth, etc.)
- [ ] All dependencies are local or API-based only
- [ ] System works in isolated network environment (except for Gemini API calls)
- [ ] Complete data processing workflow works end-to-end

### ✅ Testing Verification
- [ ] All existing tests pass
- [ ] New local mode tests pass
- [ ] System works in clean Docker environment
- [ ] Manual testing confirms all features functional
- [ ] Performance is acceptable with direct API calls

---

## Post-Conversion Validation

### Final Integration Test
```bash
# Clean environment test
docker run --rm -it \
  -e GEMINI_API_KEY=your_key \
  -e LLM_API_KEY=your_key \
  -p 8080:8080 \
  agentic-graphrag:local

# Test API endpoints
curl http://localhost:8080/agents/kg_status
curl -X POST http://localhost:8080/agents/kg_ingest \
  -H "Content-Type: application/json" \
  -d '{"data": "Local test data"}'
```

### Verification Commands
```bash
# Check for Google Cloud imports
find . -name "*.py" -exec grep -l "google\.cloud\|vertex_ai" {} \;

# Should return empty - no files should import Google Cloud

# Check dependencies
pip list | grep -E "(google-cloud|vertex)"

# Should only show google-adk and google-genai, no cloud packages

# Test system startup
python main.py --config-check
python main.py --test-only
```

---

## Time Estimates
- **Phase 1 (Analysis)**: 30 minutes
- **Phase 2 (Configuration)**: 30 minutes
- **Phase 3 (Remove Dependencies)**: 45 minutes
- **Phase 4 (Local Pattern)**: 45 minutes
- **Phase 5 (Testing)**: 30 minutes
- **Phase 6 (Documentation)**: 15 minutes

**Total Estimated Time: 3 hours 15 minutes**

## Risk Assessment: LOW
- Following proven pattern from working `kg_broker_agent` example
- Google ADK already supports local operation
- MCP integration is already local
- Configuration changes are straightforward
- Comprehensive testing plan ensures functionality

## Rollback Plan
If conversion fails:
1. Switch back to backup branch: `git checkout backup-before-local-conversion`
2. System returns to original Google Cloud dependent state
3. All original functionality preserved