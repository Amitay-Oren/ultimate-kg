# Agentic GraphRAG System - Deployment Guide

This guide covers deployment options for the Agentic GraphRAG System with A2A Protocol integration.

## Quick Start (Docker Compose)

### Prerequisites

1. **Docker and Docker Compose** installed
2. **Google Cloud Project** with Vertex AI enabled
3. **Service Account Key** with Vertex AI permissions
4. **LLM API Key** (OpenAI, Anthropic, or other)

### Environment Setup

#### Unix/Linux/macOS

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Configure environment variables:**
   ```bash
   # Required - Google Cloud
   GOOGLE_CLOUD_PROJECT=your-project-id
   VERTEX_AI_LOCATION=us-central1
   GOOGLE_APPLICATION_CREDENTIALS=./credentials/service-account.json

   # Required - LLM API Key
   LLM_API_KEY=your-openai-or-other-llm-api-key

   # Optional - Notification webhook
   WEBHOOK_URL=https://your-webhook-endpoint.com

   # Optional - Grafana password for monitoring
   GRAFANA_PASSWORD=your-secure-password
   ```

3. **Place your Google Cloud service account key:**
   ```bash
   mkdir -p credentials
   # Copy your service-account.json to credentials/
   ```

#### Windows PowerShell

1. **Copy environment template:**
   ```powershell
   Copy-Item .env.example .env
   ```

2. **Configure environment variables:**
   ```powershell
   # Edit .env file using notepad or your preferred editor
   notepad .env
   
   # Or configure directly in PowerShell
   @"
   GOOGLE_CLOUD_PROJECT=your-project-id
   VERTEX_AI_LOCATION=us-central1
   GOOGLE_APPLICATION_CREDENTIALS=./credentials/service-account.json
   LLM_API_KEY=your-openai-or-other-llm-api-key
   WEBHOOK_URL=https://your-webhook-endpoint.com
   GRAFANA_PASSWORD=your-secure-password
   "@ | Out-File -FilePath .env -Encoding UTF8
   ```

3. **Place your Google Cloud service account key:**
   ```powershell
   New-Item -ItemType Directory -Path credentials -Force
   # Copy your service-account.json to credentials\ folder
   Copy-Item "C:\path\to\your\service-account.json" "credentials\service-account.json"
   ```

### Deployment Options

#### Option 1: Complete System (Default)

**Unix/Linux/macOS:**
```bash
# Start all services including Neo4j and Cognee MCP
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f agentic-graphrag
```

**Windows PowerShell:**
```powershell
# Start all services including Neo4j and Cognee MCP
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f agentic-graphrag
```

#### Option 2: With Monitoring

**Unix/Linux/macOS:**
```bash
# Start with Prometheus and Grafana
docker-compose --profile monitoring up -d

# Access Grafana at http://localhost:3000
# Default credentials: admin / your-configured-password
```

**Windows PowerShell:**
```powershell
# Start with Prometheus and Grafana
docker-compose --profile monitoring up -d

# Access Grafana at http://localhost:3000
# Default credentials: admin / your-configured-password
```

#### Option 3: Development Mode

**Unix/Linux/macOS:**
```bash
# Start only Neo4j for development
docker-compose up -d neo4j

# Run the system locally 
python main.py
```

**Windows PowerShell:**
```powershell
# Start only Neo4j for development
docker-compose up -d neo4j

# Run the system locally 
python main.py
```

### Service Endpoints

Once deployed, the following endpoints are available:

- **A2A Server**: http://localhost:8080
- **Neo4j Browser**: http://localhost:7474 (neo4j/password123)
- **Cognee MCP**: http://localhost:8000
- **Prometheus**: http://localhost:9091 (monitoring profile)
- **Grafana**: http://localhost:3000 (monitoring profile)

## Manual Deployment

### 1. Infrastructure Setup

#### Neo4j Database
```bash
docker run -d \
  --name agentic-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password123 \
  -e NEO4J_PLUGINS='["apoc"]' \
  -v neo4j_data:/data \
  neo4j:5.15
```

#### Cognee MCP Server
```bash
# Clone and setup Cognee
git clone https://github.com/topoteretes/cognee.git
cd cognee/cognee-mcp

# Create environment
cp .env.example .env
# Edit .env with your configuration

# Install and run
uv sync --dev --all-extras
uv run src/server.py
```

### 2. Application Deployment

#### Local Development

**Unix/Linux/macOS:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run system
python main.py
```

**Windows PowerShell:**
```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
Copy-Item .env.example .env
# Edit .env with your settings using notepad .env

# Run system
python main.py
```

**Windows Command Prompt:**
```cmd
# Create virtual environment
python -m venv venv
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your settings

# Run system
python main.py
```

#### Production (systemd)
```bash
# Create systemd service
sudo cat > /etc/systemd/system/agentic-graphrag.service << EOF
[Unit]
Description=Agentic GraphRAG System
After=network.target

[Service]
Type=exec
User=agentic
WorkingDirectory=/opt/agentic-graphrag
Environment=PATH=/opt/agentic-graphrag/venv/bin
ExecStart=/opt/agentic-graphrag/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl enable agentic-graphrag
sudo systemctl start agentic-graphrag
```

## Google Cloud Run Deployment

### 1. Prepare for Cloud Run

```bash
# Build and push container
gcloud builds submit --tag gcr.io/YOUR-PROJECT/agentic-graphrag

# Or use Cloud Build
gcloud builds submit --config cloudbuild.yaml
```

### 2. Deploy to Cloud Run

```bash
gcloud run deploy agentic-graphrag \
  --image gcr.io/YOUR-PROJECT/agentic-graphrag \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 2 \
  --concurrency 100 \
  --max-instances 10 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR-PROJECT \
  --set-env-vars VERTEX_AI_LOCATION=us-central1 \
  --set-env-vars A2A_SERVER_HOST=0.0.0.0 \
  --set-env-vars A2A_NETWORK_MODE=production
```

### 3. Cloud Run with External Neo4j

For production, use Neo4j AuraDB or Google Cloud Memorystore:

```bash
gcloud run deploy agentic-graphrag \
  --image gcr.io/YOUR-PROJECT/agentic-graphrag \
  --set-env-vars GRAPH_DATABASE_URL=bolt://your-auradb-instance:7687 \
  --set-env-vars GRAPH_DATABASE_USERNAME=neo4j \
  --set-env-vars GRAPH_DATABASE_PASSWORD=your-secure-password
```

## Kubernetes Deployment

### 1. Create Kubernetes Manifests

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentic-graphrag
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agentic-graphrag
  template:
    metadata:
      labels:
        app: agentic-graphrag
    spec:
      containers:
      - name: agentic-graphrag
        image: gcr.io/YOUR-PROJECT/agentic-graphrag:latest
        ports:
        - containerPort: 8080
        env:
        - name: GOOGLE_CLOUD_PROJECT
          value: "YOUR-PROJECT"
        - name: A2A_SERVER_HOST
          value: "0.0.0.0"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: agentic-graphrag-service
spec:
  selector:
    app: agentic-graphrag
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

### 2. Deploy to Kubernetes

```bash
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml

# Check deployment
kubectl get pods
kubectl get services
```

## Validation and Testing

### 1. System Health Check

**Unix/Linux/macOS:**
```bash
# Test A2A server
curl http://localhost:8080/agents/kg_status

# Run comprehensive tests
python main.py --test-only

# Validate A2A protocol compliance
python -m agentic_graphrag.server.a2a_utils --server-url http://localhost:8080
```

**Windows PowerShell:**
```powershell
# Test A2A server
Invoke-RestMethod -Uri "http://localhost:8080/agents/kg_status" -Method GET

# Run comprehensive tests
python main.py --test-only

# Validate A2A protocol compliance
python -m agentic_graphrag.server.a2a_utils --server-url http://localhost:8080
```

### 2. Integration Testing

**Unix/Linux/macOS:**
```bash
# Test knowledge ingestion
curl -X POST http://localhost:8080/agents/kg_ingest \
  -H "Content-Type: application/json" \
  -d '{
    "data": "Alice is a 28-year-old software engineer at Google",
    "format": "text",
    "options": {
      "extract_facts": true,
      "detect_connections": true,
      "notify_threshold": 0.7
    }
  }'

# Test knowledge search
curl -X POST http://localhost:8080/agents/kg_search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "software engineer",
    "type": "hybrid",
    "limit": 10
  }'
```

**Windows PowerShell:**
```powershell
# Test knowledge ingestion
$body = @{
    data = "Alice is a 28-year-old software engineer at Google"
    format = "text"
    options = @{
        extract_facts = $true
        detect_connections = $true
        notify_threshold = 0.7
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8080/agents/kg_ingest" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

# Test knowledge search
$searchBody = @{
    query = "software engineer"
    type = "hybrid"
    limit = 10
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/agents/kg_search" `
    -Method POST `
    -ContentType "application/json" `
    -Body $searchBody
```

## Monitoring and Observability

### 1. Logs

**Unix/Linux/macOS:**
```bash
# Docker Compose logs
docker-compose logs -f agentic-graphrag

# Application logs
tail -f logs/agentic_graphrag.log

# Kubernetes logs
kubectl logs -f deployment/agentic-graphrag
```

**Windows PowerShell:**
```powershell
# Docker Compose logs
docker-compose logs -f agentic-graphrag

# Application logs
Get-Content logs/agentic_graphrag.log -Wait -Tail 50

# Kubernetes logs
kubectl logs -f deployment/agentic-graphrag
```

### 2. Metrics (Prometheus)

Access Prometheus at http://localhost:9091 to view:
- Request rates and latencies
- Error rates
- System resource usage
- Component health status

### 3. Grafana Dashboards

Access Grafana at http://localhost:3000 with configured dashboards for:
- A2A Server Performance
- Knowledge Graph Operations
- Fact Extraction Metrics
- Connection Detection Analytics
- Notification System Status

## Troubleshooting

### Common Issues

1. **Neo4j Connection Failed**

   **Unix/Linux/macOS:**
   ```bash
   # Check Neo4j status
   docker logs agentic-graphrag-neo4j
   
   # Test connection
   docker exec -it agentic-graphrag-neo4j cypher-shell -u neo4j -p password123
   ```

   **Windows PowerShell:**
   ```powershell
   # Check Neo4j status
   docker logs agentic-graphrag-neo4j
   
   # Test connection
   docker exec -it agentic-graphrag-neo4j cypher-shell -u neo4j -p password123
   ```

2. **MCP Server Not Available**

   **Unix/Linux/macOS:**
   ```bash
   # Check Cognee MCP status
   curl http://localhost:8000/health
   
   # Restart MCP server
   docker-compose restart cognee-mcp
   ```

   **Windows PowerShell:**
   ```powershell
   # Check Cognee MCP status
   Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
   
   # Restart MCP server
   docker-compose restart cognee-mcp
   ```

3. **Google Cloud Authentication**

   **Unix/Linux/macOS:**
   ```bash
   # Verify service account
   gcloud auth application-default print-access-token
   
   # Check IAM permissions
   gcloud projects get-iam-policy YOUR-PROJECT
   ```

   **Windows PowerShell:**
   ```powershell
   # Verify service account
   gcloud auth application-default print-access-token
   
   # Check IAM permissions
   gcloud projects get-iam-policy YOUR-PROJECT
   ```

4. **A2A Protocol Issues**

   **Unix/Linux/macOS:**
   ```bash
   # Validate A2A compliance
   python -m agentic_graphrag.server.a2a_utils --server-url http://localhost:8080
   
   # Check A2A server logs
   docker-compose logs agentic-graphrag | grep A2A
   ```

   **Windows PowerShell:**
   ```powershell
   # Validate A2A compliance
   python -m agentic_graphrag.server.a2a_utils --server-url http://localhost:8080
   
   # Check A2A server logs
   docker-compose logs agentic-graphrag | Select-String "A2A"
   ```

### Performance Tuning

1. **Neo4j Optimization**
   - Increase heap size: `NEO4J_dbms_memory_heap_max__size=4G`
   - Tune page cache: `NEO4J_dbms_memory_pagecache_size=2G`

2. **Application Scaling**
   - Increase concurrent requests: `A2A_MAX_CONCURRENT_REQUESTS=200`
   - Scale replicas in Kubernetes

3. **Resource Allocation**
   - Monitor CPU/memory usage
   - Adjust container resources as needed

## Security Considerations

1. **Production Deployment**
   - Use secure passwords for Neo4j
   - Enable TLS for A2A server
   - Implement proper authentication
   - Secure API keys and credentials

2. **Network Security**
   - Use private networks for internal communication
   - Implement proper firewall rules
   - Enable CORS only for trusted origins

3. **Data Protection**
   - Encrypt sensitive data at rest
   - Implement proper backup strategies
   - Follow data retention policies

## Backup and Recovery

### Database Backup
```bash
# Neo4j backup
docker exec agentic-graphrag-neo4j neo4j-admin database dump neo4j

# Restore from backup
docker exec agentic-graphrag-neo4j neo4j-admin database load neo4j
```

### Configuration Backup
```bash
# Backup environment and configuration
tar -czf backup-$(date +%Y%m%d).tar.gz .env docker-compose.yml logs/ data/
```

This deployment guide covers all major deployment scenarios. Choose the option that best fits your infrastructure and requirements.