# System Architecture

## Overview

The CRPF Centralized IT System Log Analyzer follows a multi-tier architecture designed for scalability, reliability, and security. The system uses industry-standard components from the Elastic Stack, OpenSearch, Apache Kafka, and Wazuh.

---

## Logical Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    PRESENTATION LAYER                                    │
├─────────────────┬─────────────────┬─────────────────┬───────────────────────────────────┤
│  Kibana/        │    Wazuh        │    FastAPI      │         Custom Dashboard          │
│  OpenSearch     │   Dashboard     │   REST API      │          (React/Vite)             │
│  Dashboards     │                 │                 │                                   │
└────────┬────────┴────────┬────────┴────────┬────────┴────────────────┬──────────────────┘
         │                 │                 │                         │
┌────────┴─────────────────┴─────────────────┴─────────────────────────┴──────────────────┐
│                                    ANALYTICS LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐                       │
│   │  Search &       │   │  Machine        │   │  Alerting &     │                       │
│   │  Query Engine   │   │  Learning       │   │  Notifications  │                       │
│   │                 │   │  Anomaly        │   │                 │                       │
│   └─────────────────┘   └─────────────────┘   └─────────────────┘                       │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
         │
┌────────┴────────────────────────────────────────────────────────────────────────────────┐
│                                    STORAGE LAYER                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   ┌─────────────────────────────────────────────────────────────────────────────┐       │
│   │                     Elasticsearch / OpenSearch Cluster                       │       │
│   │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                    │       │
│   │  │  system-logs  │  │  security-    │  │  metrics-     │                    │       │
│   │  │  index        │  │  alerts index │  │  index        │                    │       │
│   │  └───────────────┘  └───────────────┘  └───────────────┘                    │       │
│   └─────────────────────────────────────────────────────────────────────────────┘       │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
         │
┌────────┴────────────────────────────────────────────────────────────────────────────────┐
│                                    PROCESSING LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐                       │
│   │    Logstash     │   │  Kafka Consumer │   │  Wazuh Manager  │                       │
│   │   - Parsing     │   │   - Indexing    │   │   - Rules       │                       │
│   │   - Enrichment  │   │   - Transform   │   │   - Correlation │                       │
│   │   - Filtering   │   │                 │   │   - Decoders    │                       │
│   └─────────────────┘   └─────────────────┘   └─────────────────┘                       │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
         │
┌────────┴────────────────────────────────────────────────────────────────────────────────┐
│                                    MESSAGE QUEUE LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   ┌─────────────────────────────────────────────────────────────────────────────┐       │
│   │                           Apache Kafka Cluster                               │       │
│   │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                    │       │
│   │  │  system-logs  │  │  security-    │  │  metrics      │                    │       │
│   │  │  topic        │  │  events topic │  │  topic        │                    │       │
│   │  └───────────────┘  └───────────────┘  └───────────────┘                    │       │
│   └─────────────────────────────────────────────────────────────────────────────┘       │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
         │
┌────────┴────────────────────────────────────────────────────────────────────────────────┐
│                                    COLLECTION LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │  Winlogbeat  │  │  Filebeat    │  │  Metricbeat  │  │  Wazuh       │                 │
│  │  (Windows)   │  │  (Linux)     │  │  (Metrics)   │  │  Agents      │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘                 │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
         │
┌────────┴────────────────────────────────────────────────────────────────────────────────┐
│                                    ENDPOINT LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │   Windows    │  │    Linux     │  │   Network    │  │   Security   │                 │
│  │   Servers    │  │   Servers    │  │   Devices    │  │  Appliances  │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘                 │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    CRPF HEADQUARTERS                                     │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                           Central Ubuntu Server (VM)                               │  │
│  │                                                                                    │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │  │
│  │  │ Elasticsearch│  │   Kibana    │  │  Logstash   │  │   Kafka     │              │  │
│  │  │  :9200      │  │   :5601     │  │   :5044     │  │   :9092     │              │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘              │  │
│  │                                                                                    │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                               │  │
│  │  │   Wazuh     │  │   FastAPI   │  │  Zookeeper  │                               │  │
│  │  │  Manager    │  │   :8000     │  │   :2181     │                               │  │
│  │  │  :1514/1515 │  │             │  │             │                               │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                               │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
┌───────────────────────────┐ ┌───────────────────────────┐ ┌───────────────────────────┐
│       SECTOR A            │ │       SECTOR B            │ │       SECTOR C            │
│  ┌─────────────────────┐  │ │  ┌─────────────────────┐  │ │  ┌─────────────────────┐  │
│  │   Windows Server    │  │ │  │   Linux Server      │  │ │  │   Network Device    │  │
│  │  ┌───────────────┐  │  │ │  │  ┌───────────────┐  │  │ │  │  ┌───────────────┐  │  │
│  │  │  Winlogbeat   │  │  │ │  │  │  Filebeat     │  │  │ │  │  │  Syslog       │  │  │
│  │  │  Wazuh Agent  │  │  │ │  │  │  Metricbeat   │  │  │ │  │  │  Forwarder    │  │  │
│  │  └───────────────┘  │  │ │  │  │  Wazuh Agent  │  │  │ │  │  └───────────────┘  │  │
│  └─────────────────────┘  │ │  │  └───────────────┘  │  │ │  └─────────────────────┘  │
│                           │ │  └─────────────────────┘  │ │                           │
│  ┌─────────────────────┐  │ │                           │ │  ┌─────────────────────┐  │
│  │   Workstations      │  │ │  ┌─────────────────────┐  │ │  │   Security Appliance│  │
│  │  ┌───────────────┐  │  │ │  │   Database Server   │  │ │  │  ┌───────────────┐  │  │
│  │  │  Winlogbeat   │  │  │ │  │  ┌───────────────┐  │  │ │  │  │  Syslog       │  │  │
│  │  │  Metricbeat   │  │  │ │  │  │  Filebeat     │  │  │ │  │  │               │  │  │
│  │  └───────────────┘  │  │ │  │  └───────────────┘  │  │ │  │  └───────────────┘  │  │
│  └─────────────────────┘  │ │  └─────────────────────┘  │ │  └─────────────────────┘  │
└───────────────────────────┘ └───────────────────────────┘ └───────────────────────────┘
```

---

## Data Flow

### 1. Log Collection Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Endpoint   │    │   Agent     │    │   Kafka     │    │  Consumer   │
│  (Windows/  │───▶│ (Winlogbeat/│───▶│   Broker    │───▶│ (Indexer)   │
│   Linux)    │    │  Filebeat)  │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                 │
                                                                 ▼
                                                         ┌─────────────┐
                                                         │ Elasticsearch│
                                                         │ /OpenSearch │
                                                         └─────────────┘
```

### 2. Alternative Flow (Direct to Logstash)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Endpoint   │    │   Agent     │    │  Logstash   │    │Elasticsearch│
│  (Windows/  │───▶│ (Winlogbeat/│───▶│  Pipeline   │───▶│ /OpenSearch │
│   Linux)    │    │  Filebeat)  │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### 3. Security Alert Flow (with Wazuh)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Endpoint   │    │   Wazuh     │    │   Wazuh     │    │Elasticsearch│
│  (Windows/  │───▶│   Agent     │───▶│  Manager    │───▶│ /OpenSearch │
│   Linux)    │    │             │    │  (Analysis) │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                 │
                                                                 ▼
                                                         ┌─────────────┐
                                                         │   Kibana    │
                                                         │ (Alerting)  │
                                                         └─────────────┘
```

---

## Component Details

### Collection Layer

| Component | Purpose | Input | Output |
|-----------|---------|-------|--------|
| **Winlogbeat** | Collect Windows event logs | Windows Event Log | JSON events to Kafka/Logstash |
| **Filebeat** | Collect file-based logs | Log files | JSON events to Kafka/Logstash |
| **Metricbeat** | Collect system metrics | System stats | JSON metrics to Elasticsearch |
| **Wazuh Agent** | Security monitoring, FIM | System events | Events to Wazuh Manager |

### Message Queue Layer

| Component | Purpose | Configuration |
|-----------|---------|---------------|
| **Apache Kafka** | Buffer and distribute log events | Topics: system-logs, security-events, metrics |
| **Zookeeper** | Kafka coordination | Default configuration |

### Processing Layer

| Component | Purpose | Capabilities |
|-----------|---------|--------------|
| **Logstash** | Parse, enrich, transform logs | Grok parsing, GeoIP, enrichment |
| **Kafka Consumer** | Index logs to Elasticsearch | JSON transformation, bulk indexing |
| **Wazuh Manager** | Analyze security events | Rule-based detection, correlation |

### Storage Layer

| Component | Purpose | Indices |
|-----------|---------|---------|
| **Elasticsearch/OpenSearch** | Store and search logs | system-logs-*, wazuh-alerts-*, metricbeat-* |

### Presentation Layer

| Component | Purpose | Users |
|-----------|---------|-------|
| **Kibana/OpenSearch Dashboards** | Visualization, search | SOC analysts, administrators |
| **Wazuh Dashboard** | Security dashboards | Security team |
| **FastAPI** | Programmatic access | Applications, automation |

---

## Threat Detection Approach

### Rule-Based Detection

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Rule-Based Detection                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  Wazuh Rules    │  │  Sigma Rules    │  │  Custom Rules   │             │
│  │  - Failed auth  │  │  - MITRE ATT&CK │  │  - CRPF-specific│             │
│  │  - File changes │  │  - Known TTPs   │  │  - Policy       │             │
│  │  - Malware      │  │                 │  │    violations   │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Anomaly Detection (ML-Based)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Machine Learning Detection                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  Rare Process   │  │  Unusual Login  │  │  Network        │             │
│  │  Execution      │  │  Patterns       │  │  Anomalies      │             │
│  │                 │  │                 │  │                 │             │
│  │  Baseline:      │  │  Baseline:      │  │  Baseline:      │             │
│  │  Normal procs   │  │  Login times,   │  │  Traffic        │             │
│  │  per endpoint   │  │  locations      │  │  patterns       │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Security Architecture

### Network Security

- TLS encryption for all agent-to-server communication
- Network segmentation between management and data planes
- Firewall rules restricting access to management ports
- VPN tunnels for remote site connectivity

### Authentication & Authorization

- Elasticsearch security features enabled
- Role-based access control (RBAC)
- API key authentication for programmatic access
- Integration with Active Directory/LDAP (optional)

### Data Protection

- Encryption at rest for Elasticsearch indices
- Audit logging for all administrative actions
- Secure backup and recovery procedures
- Data retention and purging policies

---

## Scalability Considerations

### Horizontal Scaling

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Scaled Deployment                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Elasticsearch Cluster:                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                          │
│  │ Data Node 1 │  │ Data Node 2 │  │ Data Node 3 │                          │
│  └─────────────┘  └─────────────┘  └─────────────┘                          │
│                                                                              │
│  Kafka Cluster:                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                          │
│  │  Broker 1   │  │  Broker 2   │  │  Broker 3   │                          │
│  └─────────────┘  └─────────────┘  └─────────────┘                          │
│                                                                              │
│  Logstash Instances:                                                         │
│  ┌─────────────┐  ┌─────────────┐                                           │
│  │ Logstash 1  │  │ Logstash 2  │  (behind load balancer)                   │
│  └─────────────┘  └─────────────┘                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Capacity Planning

| Metric | Small Deployment | Medium Deployment | Large Deployment |
|--------|-----------------|-------------------|------------------|
| Endpoints | 50-100 | 100-500 | 500-2000+ |
| Events/sec | 1,000 | 5,000 | 20,000+ |
| ES Nodes | 1 | 3 | 5+ |
| Kafka Brokers | 1 | 3 | 5+ |
| Storage/Day | 10 GB | 50 GB | 200+ GB |
