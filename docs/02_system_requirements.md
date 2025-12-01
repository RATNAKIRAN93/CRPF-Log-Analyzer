# System Requirements

## Hardware Requirements

### Central Server (Elasticsearch/OpenSearch Cluster)

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 4 cores | 8+ cores |
| **RAM** | 8 GB | 16-32 GB |
| **Storage** | 100 GB SSD | 500 GB+ SSD |
| **Network** | 1 Gbps | 10 Gbps |

> **Note**: For production deployments handling high log volumes, consider a 3-node Elasticsearch cluster with dedicated master, data, and coordinating nodes.

### Log Processing Server (Logstash/Kafka)

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 2 cores | 4+ cores |
| **RAM** | 4 GB | 8 GB |
| **Storage** | 50 GB SSD | 100 GB SSD |
| **Network** | 1 Gbps | 10 Gbps |

### Endpoint Agents (Beats/Wazuh)

| Component | Minimum |
|-----------|---------|
| **CPU** | 1 core |
| **RAM** | 512 MB |
| **Storage** | 1 GB |
| **Network** | 100 Mbps |

---

## Software Requirements

### Operating Systems

| Component | Supported OS |
|-----------|--------------|
| **Central Server** | Ubuntu 22.04 LTS, RHEL 8+, CentOS Stream 8+ |
| **Windows Endpoints** | Windows Server 2016+, Windows 10/11 |
| **Linux Endpoints** | Ubuntu 18.04+, RHEL 7+, CentOS 7+, Debian 10+ |

### Container Runtime

| Software | Version |
|----------|---------|
| **Docker** | 24.0+ |
| **Docker Compose** | 2.20+ |

### Core Stack Components

| Component | Version | Purpose |
|-----------|---------|---------|
| **Elasticsearch** | 8.x / 9.x | Search and analytics engine |
| **OpenSearch** | 2.9.x | Alternative search engine |
| **Kibana** | 8.x / 9.x | Visualization and dashboards |
| **OpenSearch Dashboards** | 2.9.x | Alternative visualization |
| **Logstash** | 8.x / 9.x | Log processing pipeline |
| **Apache Kafka** | 3.5+ | Message queue and buffering |
| **Zookeeper** | 3.8+ | Kafka coordination |

### Agent Components

| Agent | Version | Purpose |
|-------|---------|---------|
| **Winlogbeat** | 8.x | Windows event log collection |
| **Filebeat** | 8.x | File-based log collection |
| **Metricbeat** | 8.x | System metrics collection |
| **Wazuh Agent** | 4.x | Security monitoring and HIDS |

### Backend Services

| Component | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.10+ | FastAPI backend |
| **FastAPI** | 0.100+ | REST API framework |
| **opensearch-py** | 2.x | OpenSearch Python client |

---

## Network Ports

### Central Server Ports

| Port | Protocol | Service | Description |
|------|----------|---------|-------------|
| 9200 | TCP | Elasticsearch/OpenSearch | REST API |
| 9300 | TCP | Elasticsearch | Node-to-node communication |
| 5601 | TCP | Kibana/OpenSearch Dashboards | Web UI |
| 5044 | TCP | Logstash | Beats input |
| 9092 | TCP | Kafka | Broker communication |
| 2181 | TCP | Zookeeper | Coordination |
| 8000 | TCP | FastAPI | REST API |
| 9600 | TCP | Logstash | Monitoring API |

### Wazuh Ports (if deployed)

| Port | Protocol | Service | Description |
|------|----------|---------|-------------|
| 1514 | TCP/UDP | Wazuh Manager | Agent communication |
| 1515 | TCP | Wazuh Manager | Agent enrollment |
| 1516 | TCP | Wazuh Manager | Cluster communication |
| 55000 | TCP | Wazuh API | REST API |

### Firewall Configuration

```bash
# Allow Elasticsearch
sudo ufw allow 9200/tcp

# Allow Kibana
sudo ufw allow 5601/tcp

# Allow Logstash Beats input
sudo ufw allow 5044/tcp

# Allow Kafka
sudo ufw allow 9092/tcp

# Allow FastAPI
sudo ufw allow 8000/tcp

# Allow Wazuh agent communication (if using Wazuh)
sudo ufw allow 1514/tcp
sudo ufw allow 1515/tcp
```

---

## Supported Log Sources

### Windows Systems

| Log Type | Source | Agent |
|----------|--------|-------|
| Security Events | Windows Security Log | Winlogbeat |
| System Events | Windows System Log | Winlogbeat |
| Application Events | Windows Application Log | Winlogbeat |
| PowerShell Logs | Microsoft-Windows-PowerShell | Winlogbeat |
| Sysmon Events | Microsoft-Windows-Sysmon | Winlogbeat |

### Linux Systems

| Log Type | Source | Agent |
|----------|--------|-------|
| Authentication | /var/log/auth.log, /var/log/secure | Filebeat |
| System Logs | /var/log/syslog, /var/log/messages | Filebeat |
| Application Logs | /var/log/application/*.log | Filebeat |
| Audit Logs | /var/log/audit/audit.log | Filebeat |
| Kernel Logs | /var/log/kern.log | Filebeat |

### Network Devices

| Device Type | Protocol | Collection Method |
|-------------|----------|-------------------|
| Firewalls | Syslog | Logstash syslog input |
| Routers | Syslog | Logstash syslog input |
| Switches | Syslog | Logstash syslog input |
| IDS/IPS | Syslog | Logstash syslog input |

---

## Security Assumptions

### Network Security

- All agent-to-server communication uses TLS encryption
- Network segmentation between public and management networks
- Firewall rules limit access to management ports
- VPN connectivity for remote unit agents

### Authentication & Authorization

- Role-based access control (RBAC) enabled on Elasticsearch
- Strong passwords for all service accounts
- API keys for programmatic access
- Multi-factor authentication for administrative access

### Data Security

- Logs encrypted at rest using Elasticsearch encryption
- Audit logging enabled for all administrative actions
- Regular backup of indices and configurations
- Data retention policies enforced

### Endpoint Security

- Agents run with minimal required privileges
- Agent configurations protected from tampering
- Secure enrollment process for new agents
- Regular agent updates and patching

---

## Capacity Planning

### Log Volume Estimation

| Source Type | Events/Day (per endpoint) | Size/Day (per endpoint) |
|-------------|---------------------------|------------------------|
| Windows Security | 10,000 - 50,000 | 10 - 50 MB |
| Linux Auth | 1,000 - 10,000 | 1 - 10 MB |
| System Metrics | 86,400 | 10 - 20 MB |
| Network Syslog | 10,000 - 100,000 | 10 - 100 MB |

### Storage Requirements

```
Daily Storage = (Events/Day × Average Event Size) × Number of Endpoints

Example:
- 100 Windows endpoints @ 30 MB/day = 3 GB/day
- 50 Linux servers @ 20 MB/day = 1 GB/day
- System metrics @ 15 MB/day × 150 = 2.25 GB/day
- Total: ~6.25 GB/day raw

With indexing overhead (1.5x): ~10 GB/day
90-day retention: ~900 GB storage
```

### Memory Sizing

```
Elasticsearch Heap = 50% of available RAM (max 32 GB)

For 16 GB RAM server:
- Elasticsearch: 8 GB heap
- Kibana: 2 GB
- Logstash: 2 GB
- OS and other: 4 GB
```
