# Installation Guide

This guide provides step-by-step instructions to install and set up the CRPF Log Analyzer system.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start (Docker)](#quick-start-docker)
- [Installation via Git](#installation-via-git)
- [Manual Installation](#manual-installation)
- [Configuration](#configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **RAM** | 8 GB | 16 GB |
| **Disk Space** | 50 GB | 100 GB |
| **CPU Cores** | 4 cores | 8 cores |

### Software Requirements

- **Operating System**: Ubuntu 22.04+ or any Linux with Docker support
- **Docker**: Version 20.10+ ([Install Docker](https://docs.docker.com/engine/install/))
- **Docker Compose**: Version 2.0+ ([Install Docker Compose](https://docs.docker.com/compose/install/))
- **Git**: Latest version ([Install Git](https://git-scm.com/downloads))
- **Python**: 3.9+ (for local development only)

### Network Ports

Ensure the following ports are available:

| Port | Service | Description |
|------|---------|-------------|
| `9200` | Elasticsearch/OpenSearch | Data storage and search |
| `5601` | Kibana/OpenSearch Dashboards | Visualization interface |
| `5044` | Logstash | Beats input |
| `9092` | Kafka | Message queue |
| `2181` | Zookeeper | Kafka coordination |
| `8000` | FastAPI | REST API server |
| `1514/1515` | Wazuh | Agent communication (optional) |

---

## Quick Start (Docker)

The fastest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/RATNAKIRAN93/CRPF-Log-Analyzer.git
cd CRPF-Log-Analyzer

# Start all services
docker compose up -d

# Wait for services to be healthy (approximately 2-3 minutes)
docker compose ps

# View logs
docker compose logs -f
```

**Access Points:**
- **OpenSearch Dashboards**: http://localhost:5601
- **FastAPI Docs**: http://localhost:8000/docs
- **Elasticsearch Health**: http://localhost:9200

---

## Installation via Git

### Step 1: Clone the Repository

```bash
# Clone with HTTPS
git clone https://github.com/RATNAKIRAN93/CRPF-Log-Analyzer.git

# OR clone with SSH
git clone git@github.com:RATNAKIRAN93/CRPF-Log-Analyzer.git

# Navigate to project directory
cd CRPF-Log-Analyzer
```

### Step 2: Set Up Environment

```bash
# Copy example environment file (if available)
cp .env.example .env

# Edit environment variables as needed
nano .env
```

### Step 3: Install Python Dependencies (Optional - for local development)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies from root requirements
pip install -r requirements.txt
```

### Step 4: Start Services with Docker Compose

```bash
# Build and start all services
docker compose up -d --build

# Check service status
docker compose ps

# View logs for specific service
docker compose logs -f opensearch
docker compose logs -f kafka
docker compose logs -f consumer
```

### Step 5: Verify Installation

```bash
# Check OpenSearch cluster health
curl -X GET "http://localhost:9200/_cluster/health?pretty"

# Check Kafka topics
docker compose exec kafka kafka-topics.sh --list --bootstrap-server localhost:9092

# Test FastAPI endpoint
curl http://localhost:8000/health
```

---

## Manual Installation

For advanced users who want to install components individually:

### Install OpenSearch

```bash
# Using Docker
docker run -d \
  --name opensearch \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "DISABLE_SECURITY_PLUGIN=true" \
  opensearchproject/opensearch:2.9.0
```

### Install Kafka

```bash
# Start Zookeeper
docker run -d \
  --name zookeeper \
  -p 2181:2181 \
  -e ZOOKEEPER_CLIENT_PORT=2181 \
  confluentinc/cp-zookeeper:7.5.0

# Start Kafka
docker run -d \
  --name kafka \
  -p 9092:9092 \
  -e KAFKA_BROKER_ID=1 \
  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  --link zookeeper \
  confluentinc/cp-kafka:7.5.0
```

### Install FastAPI Service

```bash
cd fastapi

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenSearch Configuration
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_INDEX=system-logs

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=system-logs

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Logging
LOG_LEVEL=INFO
```

### OpenSearch Dashboard Configuration

1. Open OpenSearch Dashboards at `http://localhost:5601`
2. Go to **Stack Management** → **Index Patterns**
3. Create index pattern: `system-logs*`
4. Select `@timestamp` as the time field

---

## Verification

### Health Checks

```bash
# Check all Docker containers
docker compose ps

# Expected output: All services should be "Up" and "healthy"
```

### Data Ingestion Test

1. Open OpenSearch Dashboards at `http://localhost:5601`
2. Navigate to **Discover**
3. Select the `system-logs*` index pattern
4. You should see logs flowing from the simulated producers

### API Test

```bash
# Test search endpoint
curl -X GET "http://localhost:8000/search?q=error" -H "accept: application/json"

# Test health endpoint
curl -X GET "http://localhost:8000/health"
```

---

## Troubleshooting

### Common Issues

#### Services Won't Start

```bash
# Check container logs
docker compose logs <service-name>

# Restart specific service
docker compose restart <service-name>

# Rebuild containers
docker compose up -d --build --force-recreate
```

#### Port Conflicts

```bash
# Find process using port
sudo lsof -i :9200

# Kill process (replace PID)
sudo kill -9 <PID>
```

#### Memory Issues

```bash
# Increase Docker memory limit
# Edit Docker Desktop settings to allocate more RAM

# Or set OpenSearch heap size
docker compose exec opensearch bash
export OPENSEARCH_JAVA_OPTS="-Xms2g -Xmx2g"
```

#### Kafka Connection Issues

```bash
# Check if Kafka is running
docker compose logs kafka

# Check Zookeeper
docker compose logs zookeeper

# Restart Kafka stack
docker compose restart zookeeper kafka
```

### Getting Help

- Check the [Troubleshooting Guide](docs/07_troubleshooting.md)
- Open an issue on [GitHub](https://github.com/RATNAKIRAN93/CRPF-Log-Analyzer/issues)
- Review Docker logs: `docker compose logs -f`

---

## Next Steps

After successful installation:

1. **Configure Agents**: Set up Beats agents on endpoints ([Deployment Guide](docs/04_deployment_guide.md))
2. **Create Dashboards**: Import pre-built dashboards ([User Manual](docs/05_user_manual.md))
3. **Set Up Alerts**: Configure detection rules ([Architecture](docs/03_architecture.md))
4. **API Integration**: Use the REST API ([API Endpoints](docs/06_api_endpoints.md))

---

## Uninstallation

To remove all containers and data:

```bash
# Stop and remove containers
docker compose down

# Remove volumes (WARNING: This deletes all data)
docker compose down -v

# Remove images
docker compose down --rmi all
```
