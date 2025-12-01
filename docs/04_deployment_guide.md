# Deployment Guide

This guide provides step-by-step instructions for deploying the CRPF Centralized IT System Log Analyzer.

---

## Prerequisites

Before starting the deployment, ensure you have:

- [ ] Ubuntu 22.04 LTS server (or compatible Linux distribution)
- [ ] Docker 24.0+ installed
- [ ] Docker Compose 2.20+ installed
- [ ] Minimum 8 GB RAM (16 GB recommended)
- [ ] Minimum 50 GB disk space (SSD recommended)
- [ ] Root or sudo access
- [ ] Network connectivity to endpoints

### Install Docker (if not installed)

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install prerequisites
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add current user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

---

## Deployment Options

The CRPF Log Analyzer supports two deployment configurations:

1. **OpenSearch Stack** (Recommended for new deployments)
   - OpenSearch + OpenSearch Dashboards + Kafka + FastAPI
   - Uses the main `docker-compose.yml`

2. **ELK Stack** (Traditional Elastic Stack)
   - Elasticsearch + Kibana + Logstash
   - Uses `docker-elk/docker-compose.yml`

---

## Option 1: OpenSearch Stack Deployment

### Step 1: Clone the Repository

```bash
git clone https://github.com/RATNAKIRAN93/CRPF-Log-Analyzer.git
cd CRPF-Log-Analyzer
```

### Step 2: Review Configuration

The main `docker-compose.yml` includes:
- **Zookeeper**: Kafka coordination
- **Kafka**: Message queue for log buffering
- **OpenSearch**: Search and analytics engine
- **OpenSearch Dashboards**: Visualization UI
- **Producer1/Producer2**: Simulated log generators (for testing)
- **Consumer**: Kafka to OpenSearch indexer
- **FastAPI**: REST API service

### Step 3: Start the Stack

```bash
# Start all services
docker compose up -d

# Watch logs to ensure services start correctly
docker compose logs -f

# Press Ctrl+C to exit log viewing
```

### Step 4: Verify Services

```bash
# Check service status
docker compose ps

# Expected output: all services should show "running" or "healthy"
```

Wait approximately 2-3 minutes for all services to initialize.

### Step 5: Access Dashboards

| Service | URL | Credentials |
|---------|-----|-------------|
| OpenSearch Dashboards | http://localhost:5601 | No auth required (security disabled for demo) |
| OpenSearch API | http://localhost:9200 | No auth required |
| FastAPI Docs | http://localhost:8000/docs | No auth required |

### Step 6: Create Index Pattern

1. Open OpenSearch Dashboards at `http://localhost:5601`
2. Navigate to **Stack Management** → **Index Patterns**
3. Click **Create index pattern**
4. Enter `system-logs*` as the pattern
5. Select `timestamp` as the time field
6. Click **Create index pattern**

### Step 7: Verify Data

1. Navigate to **Discover** in OpenSearch Dashboards
2. Select the `system-logs*` index pattern
3. You should see log events from the simulated producers

---

## Option 2: ELK Stack Deployment

### Step 1: Clone and Navigate

```bash
git clone https://github.com/RATNAKIRAN93/CRPF-Log-Analyzer.git
cd CRPF-Log-Analyzer/docker-elk
```

### Step 2: Configure Environment Variables

```bash
# Copy the environment file
cp .env .env.local

# Edit passwords (IMPORTANT: Change these for production!)
nano .env.local
```

Key variables to configure:
```bash
ELASTIC_VERSION=9.1.4
ELASTIC_PASSWORD='YourStrongPassword123!'
LOGSTASH_INTERNAL_PASSWORD='YourStrongPassword123!'
KIBANA_SYSTEM_PASSWORD='YourStrongPassword123!'
```

### Step 3: Initialize Elasticsearch Security

```bash
# Run the setup service to initialize passwords
docker compose --profile setup up setup

# Wait for setup to complete (check logs)
docker compose logs setup
```

### Step 4: Start the ELK Stack

```bash
# Start core services
docker compose up -d

# Verify services
docker compose ps
```

### Step 5: Access Kibana

| Service | URL | Credentials |
|---------|-----|-------------|
| Kibana | http://localhost:5601 | elastic / (password from .env) |
| Elasticsearch | http://localhost:9200 | elastic / (password from .env) |
| Logstash | http://localhost:9600 | N/A (monitoring only) |

---

## Agent Installation

### Installing Metricbeat (Linux)

```bash
# Download Metricbeat
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-8.11.0-amd64.deb

# Install
sudo dpkg -i metricbeat-8.11.0-amd64.deb

# Configure (edit /etc/metricbeat/metricbeat.yml)
sudo nano /etc/metricbeat/metricbeat.yml
```

Configuration for Metricbeat:
```yaml
output.elasticsearch:
  hosts: ["<CENTRAL-SERVER-IP>:9200"]
  username: "elastic"
  password: "<your-password>"

setup.kibana:
  host: "<CENTRAL-SERVER-IP>:5601"
```

```bash
# Enable modules
sudo metricbeat modules enable system

# Setup dashboards (optional)
sudo metricbeat setup

# Start Metricbeat
sudo systemctl enable metricbeat
sudo systemctl start metricbeat
```

### Installing Filebeat (Linux)

```bash
# Download Filebeat
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.11.0-amd64.deb

# Install
sudo dpkg -i filebeat-8.11.0-amd64.deb

# Configure
sudo nano /etc/filebeat/filebeat.yml
```

Configuration for Filebeat:
```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/*.log
    - /var/log/syslog
    - /var/log/auth.log

output.elasticsearch:
  hosts: ["<CENTRAL-SERVER-IP>:9200"]
  username: "elastic"
  password: "<your-password>"
```

```bash
# Enable modules
sudo filebeat modules enable system

# Setup
sudo filebeat setup

# Start
sudo systemctl enable filebeat
sudo systemctl start filebeat
```

### Installing Winlogbeat (Windows)

1. Download Winlogbeat from [Elastic Downloads](https://www.elastic.co/downloads/beats/winlogbeat)

2. Extract to `C:\Program Files\Winlogbeat`

3. Edit `winlogbeat.yml`:
```yaml
winlogbeat.event_logs:
  - name: Application
  - name: Security
  - name: System

output.elasticsearch:
  hosts: ["<CENTRAL-SERVER-IP>:9200"]
  username: "elastic"
  password: "<your-password>"
```

4. Install as service (run PowerShell as Administrator):
```powershell
cd "C:\Program Files\Winlogbeat"
.\install-service-winlogbeat.ps1

# Start the service
Start-Service winlogbeat
```

---

## Verify Agent Data

### Check Indices

```bash
# For OpenSearch
curl -X GET "http://localhost:9200/_cat/indices?v"

# For Elasticsearch (with auth)
curl -u elastic:<password> -X GET "http://localhost:9200/_cat/indices?v"
```

### Check Data in Dashboards

1. Navigate to **Discover** in Kibana/OpenSearch Dashboards
2. Create index patterns for:
   - `metricbeat-*`
   - `filebeat-*`
   - `winlogbeat-*`
3. Verify events are appearing with recent timestamps

---

## Production Considerations

### Security Hardening

- [ ] Change all default passwords
- [ ] Enable TLS for Elasticsearch/OpenSearch
- [ ] Configure firewall rules
- [ ] Enable audit logging
- [ ] Set up role-based access control

### Performance Tuning

- [ ] Increase JVM heap size for Elasticsearch
- [ ] Configure index lifecycle management (ILM)
- [ ] Set up hot-warm-cold architecture for large deployments
- [ ] Enable index compression

### Monitoring

- [ ] Set up Metricbeat to monitor the stack itself
- [ ] Configure alerting for service health
- [ ] Set up backup procedures

---

## Stopping the Stack

```bash
# Stop services (preserves data)
docker compose stop

# Stop and remove containers (preserves volumes)
docker compose down

# Stop and remove everything including data (DESTRUCTIVE!)
docker compose down -v
```

---

## Troubleshooting

If you encounter issues during deployment, refer to [07_troubleshooting.md](07_troubleshooting.md) for common problems and solutions.

### Quick Diagnostics

```bash
# Check container logs
docker compose logs <service-name>

# Check Elasticsearch/OpenSearch cluster health
curl -X GET "http://localhost:9200/_cluster/health?pretty"

# Check disk space
df -h

# Check memory usage
free -h

# Check Docker resource usage
docker stats
```
