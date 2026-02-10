
# CRPF-Log-Analyzer

CRPF units/offices and personnel are deployed in different locations across India. This centralized system provides automated log analysis from IT systems deployed at different locations, enabling security experts to detect threats and breaches efficiently.

## Features

### Core Features
- **Centralized Log Collection**: Collects logs from multiple endpoints using Kafka message queuing
- **Real-time Processing**: Consumer service indexes logs to OpenSearch for fast search
- **Search API**: FastAPI-based REST API for log queries

### AI Agent Features (New!)
The system now includes an intelligent **Log Analysis Agent** that provides:

- **Threat Detection**: Automatically identifies security threats such as:
  - Brute force attacks (failed password attempts)
  - Unauthorized access attempts
  - Network anomalies
  - Service failures
  - Configuration changes
  - Malware/attack indicators (SQL injection, XSS, etc.)

- **Anomaly Detection**: Identifies unusual patterns including:
  - High error rates (above threshold)
  - Multiple failed login attempts per user
  - Users accessing from multiple source IPs

- **Risk Scoring**: Calculates an overall risk score (0-100) based on detected threats and anomalies

- **Automated Recommendations**: Generates actionable security recommendations based on analysis

- **Report Generation**: Creates human-readable text reports for security teams

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   Endpoint 1    │     │   Endpoint 2    │
│   (Producer)    │     │   (Producer)    │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
              ┌──────────────┐
              │    Kafka     │
              │   (Queue)    │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │   Consumer   │
              │  (Indexer)   │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │  OpenSearch  │
              │  (Storage)   │
              └──────┬───────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│    FastAPI      │     │   OpenSearch    │
│  + AI Agent     │     │   Dashboards    │
└─────────────────┘     └─────────────────┘
```

## API Endpoints

### Search Endpoint
- `GET /search?q=<query>` - Search logs using query string syntax

### Agent Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agent/status` | GET | Get agent status and capabilities |
| `/agent/analyze` | POST | Comprehensive log analysis |
| `/agent/analyze/quick` | GET | Quick analysis with query parameters |
| `/agent/threats` | POST | Get threat summary |
| `/agent/threats/quick` | GET | Quick threat summary |
| `/agent/report` | GET | Generate text report |
| `/agent/endpoints` | GET | Analysis by endpoint |
| `/agent/users` | GET | User activity analysis |
| `/agent/anomalies` | GET | Detected anomalies |
| `/agent/recommendations` | GET | Security recommendations |
| `/agent/history` | GET | Analysis history |
| `/health` | GET | Health check |

### Example Usage

```bash
# Check agent status
curl http://localhost:8000/agent/status

# Quick analysis of last 24 hours
curl "http://localhost:8000/agent/analyze/quick?hours=24"

# Get threat summary
curl http://localhost:8000/agent/threats/quick

# Generate security report
curl http://localhost:8000/agent/report

# Get recommendations
curl http://localhost:8000/agent/recommendations
```

## Quick Start

### Prerequisites
- Docker and Docker Compose

### Running the System

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Access services
# - FastAPI: http://localhost:8000
# - OpenSearch Dashboards: http://localhost:5601
# - OpenSearch: http://localhost:9200
```

### API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Components

### Producers (`/producers/producer`)
Simulates log generation from endpoints. Generates events including:
- User logins
- Failed password attempts
- File deletions
- Process starts
- Network connections
- Service crashes
- Configuration changes

### Consumer (`/consumer`)
Consumes logs from Kafka and indexes them to OpenSearch.

### FastAPI (`/fastapi`)
REST API with:
- Log search functionality
- AI-powered log analysis agent
- Threat detection and anomaly identification
- Report generation

## Development

### Running Tests

```bash
cd fastapi
pip install -r requirements.txt
pytest -v
```

### Project Structure

```
CRPF-Log-Analyzer/
├── docker-compose.yml      # Main orchestration
├── consumer/               # Kafka to OpenSearch indexer
│   ├── Dockerfile
│   ├── consumer.py
│   └── requirements.txt
├── fastapi/                # API and Agent
│   ├── Dockerfile
│   ├── main.py            # FastAPI application
│   ├── agent.py           # AI Log Analysis Agent
│   ├── test_agent.py      # Agent unit tests
│   ├── test_api.py        # API integration tests
│   └── requirements.txt
└── producers/producer/     # Log generator
    ├── Dockerfile
    ├── produce.py
    └── requirements.txt
```

## Security Considerations

- The agent is designed for internal network use
- OpenSearch security is disabled for development (enable for production)
- Review and customize threat patterns for your environment
- Adjust anomaly thresholds based on your baseline

## License

See LICENSE file for details.

=======
# CRPF Centralized IT System Log Analyzer

**Centralized, AI-assisted SIEM using ELK, Wazuh, and Beats for the Central Reserve Police Force (CRPF).**

A centralized security log monitoring platform built on the Elastic Stack (Elasticsearch, Logstash, Kibana), OpenSearch, Kafka, and Wazuh to address **SIH Problem Statement 1408: IT System Log Analyzer (Blockchain & Cybersecurity)**.

---

## Problem and Motivation

CRPF units and offices are deployed across diverse locations throughout India. Currently, there is **no centralized system** for experts to collect, analyze, and monitor IT system logs for threat detection and incident response.

### Key Challenges:
- **Fragmented visibility**: Logs scattered across multiple locations with no unified view
- **Delayed detection**: Security breaches go unnoticed due to lack of real-time monitoring
- **Difficult investigations**: No centralized evidence for forensic analysis and case building
- **Resource constraints**: Limited cybersecurity expertise at individual unit level

This leads to delayed detection of breaches, fragmented security posture, and difficulty in building digital evidence for investigations.

---

## Solution Overview

This project provides a **centralized log analysis system** that:

- **Collects logs** from endpoints (Windows/Linux), servers, and network devices using Beats agents, Wazuh agents, and Kafka-based log producers
- **Normalizes, enriches, and indexes** logs into a central Elasticsearch/OpenSearch cluster
- **Detects threats** through Wazuh rules, correlation logic, and Elastic ML anomaly detection
- **Presents SOC-ready dashboards** and reports for CRPF cyber security cells and unit IT officers

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Centralized Log Ingestion** | Winlogbeat, Filebeat, Metricbeat agents plus Wazuh agents across CRPF sites, with Kafka-based buffering |
| **Real-time Dashboards** | System health monitoring and security alert visualization via Kibana/OpenSearch Dashboards |
| **Threat Detection Engine** | Wazuh correlation rules, Sigma-style detections, and Elastic ML jobs for anomaly-based alerts |
| **Rule-based Detection** | Failed logon detection, privilege escalation, lateral movement patterns, unusual network connections |
| **Role-based Access Control** | Views tailored for SOC analysts, administrators, and unit IT staff |
| **Incident Timeline & Reporting** | Dashboards and saved searches to reconstruct attack paths and export evidence |
| **Scalable Architecture** | Containerized deployment with Docker Compose for easy scaling |
| **REST API** | FastAPI backend for programmatic access to alerts, search, and analytics |

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CRPF Log Analyzer Architecture                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Windows Servers │    │  Linux Servers   │    │ Network Devices  │
│  ┌────────────┐  │    │  ┌────────────┐  │    │  ┌────────────┐  │
│  │ Winlogbeat │  │    │  │ Filebeat   │  │    │  │ Syslog     │  │
│  │ Wazuh Agent│  │    │  │ Metricbeat │  │    │  │ Forwarder  │  │
│  └─────┬──────┘  │    │  │ Wazuh Agent│  │    │  └─────┬──────┘  │
└────────┼─────────┘    │  └─────┬──────┘  │    └────────┼─────────┘
         │              └────────┼─────────┘             │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      Apache Kafka       │
                    │   (Message Buffering)   │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│    Logstash     │   │  Kafka Consumer │   │  Wazuh Manager  │
│  (Processing)   │   │   (Indexing)    │   │   (Analysis)    │
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Elasticsearch /   │
                    │     OpenSearch      │
                    │  (Storage & Search) │
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│     Kibana /    │   │    FastAPI      │   │  Wazuh         │
│   OpenSearch    │   │   REST API      │   │  Dashboard     │
│   Dashboards    │   │                 │   │                │
└─────────────────┘   └─────────────────┘   └─────────────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │    SOC Analysts     │
                    │   CRPF Cyber Cell   │
                    │   Unit IT Officers  │
                    └─────────────────────┘
```

For detailed architecture documentation, see [docs/03_architecture.md](docs/03_architecture.md).

---

## Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Search & Analytics** | Elasticsearch / OpenSearch | 9.x / 2.9.0 |
| **Visualization** | Kibana / OpenSearch Dashboards | 9.x / 2.9.0 |
| **Log Processing** | Logstash | 9.x |
| **Message Queue** | Apache Kafka | 3.5 |
| **Security Platform** | Wazuh Manager | 4.x |
| **Agents** | Winlogbeat, Filebeat, Metricbeat, Wazuh agents | Latest |
| **Backend API** | Python FastAPI | 3.x |
| **Container Platform** | Docker & Docker Compose | Latest |
| **Optional Frontend** | React/Vite | - |

---

## Getting Started (Local Lab)

### Prerequisites

- **Operating System**: Ubuntu 22.04+ or any Linux with Docker support
- **Hardware**: Minimum 8-12 GB RAM, 50+ GB disk space
- **Software**: Docker and Docker Compose installed
- **Network Ports**:
  - `9200`: Elasticsearch/OpenSearch
  - `5601`: Kibana/OpenSearch Dashboards
  - `5044`: Logstash Beats input
  - `9092`: Kafka
  - `2181`: Zookeeper
  - `8000`: FastAPI
  - `1514/1515`: Wazuh agent communication (if using Wazuh)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/RATNAKIRAN93/CRPF-Log-Analyzer.git
cd CRPF-Log-Analyzer

# Start the main stack (OpenSearch + Kafka + Producers + Consumer + API)
docker compose up -d

# Wait for services to be healthy (approximately 2-3 minutes)
docker compose ps

# Access the dashboards
# OpenSearch Dashboards: http://localhost:5601
# FastAPI Docs: http://localhost:8000/docs
# Elasticsearch (health check): http://localhost:9200
```

### Alternative: ELK Stack Deployment

```bash
cd docker-elk

# Copy and configure environment variables
cp .env .env.local
# Edit .env.local to set passwords

# Start ELK stack
docker compose up -d

# Access Kibana: http://localhost:5601
# Default credentials: elastic / changeme
```

### Verify Data Ingestion

1. Open OpenSearch Dashboards at `http://localhost:5601`
2. Go to **Discover** → Create index pattern `system-logs*`
3. You should see logs flowing from the simulated producers

For detailed deployment instructions, see [docs/04_deployment_guide.md](docs/04_deployment_guide.md).

---

## Use Cases / User Journeys

### 1. Investigate Failed Login Storm on CRPF HQ Server
- SOC analyst receives alert for multiple failed login attempts
- Opens Kibana/OpenSearch Dashboards and filters by `level:ERROR` and `message:"Failed password"`
- Identifies source IPs and affected endpoints
- Creates incident timeline for investigation

### 2. Monitor Endpoint Health Across Remote Units
- Unit IT Officer views system health dashboard
- Checks CPU, memory, disk usage across all monitored endpoints
- Identifies servers with high resource utilization
- Takes preventive action before outages occur

### 3. View SOC Dashboard for Last 24 Hours
- SOC Team Lead opens main security dashboard
- Reviews alert summary: Critical, High, Medium, Low
- Drills down into specific alert categories
- Assigns incidents to analysts for investigation

### 4. Search for Specific Security Events
- Analyst uses FastAPI endpoint to search logs programmatically
- Query: `GET /search?q=level:ERROR AND user:admin`
- Exports results for reporting

---

## Project Structure

```
CRPF-Log-Analyzer/
├── README.md                 # This file - project overview and quick start
├── docs/                     # Detailed documentation
│   ├── 01_problem_statement.md
│   ├── 02_system_requirements.md
│   ├── 03_architecture.md
│   ├── 04_deployment_guide.md
│   ├── 05_user_manual.md
│   ├── 06_api_endpoints.md
│   └── 07_troubleshooting.md
├── backend/                  # Backend services and scripts
│   ├── api/                  # FastAPI wrapper for Elasticsearch/Wazuh queries
│   └── scripts/              # Setup scripts, indexing jobs
├── frontend/                 # Optional web UI
│   └── dashboard-ui/         # React/Vite custom dashboard
├── infra/                    # Infrastructure configurations
│   ├── docker-compose.yml    # Main orchestration file (reference)
│   ├── metricbeat/           # Metricbeat configurations
│   ├── filebeat/             # Filebeat configurations
│   ├── winlogbeat/           # Winlogbeat configurations
│   └── configs/              # Additional configuration files
├── examples/                 # Sample data and exports
│   ├── sample_logs/          # Example log files for testing
│   ├── saved_objects/        # Exported Kibana dashboards, index patterns
│   ├── dashboards/           # Dashboard JSON exports
│   └── screenshots/          # UI screenshots for documentation
├── docker-compose.yml        # Main Docker Compose (OpenSearch + Kafka stack)
├── docker-elk/               # Traditional ELK stack deployment
├── fastapi/                  # FastAPI search service
├── consumer/                 # Kafka consumer for log indexing
├── producers/                # Simulated log producers
└── LICENSE
```

---

## Roadmap

- [ ] **Enhanced ML Jobs**: Rare process execution detection, data exfiltration anomalies
- [ ] **Wazuh Integration**: Full Wazuh manager deployment with agent enrollment
- [ ] **Ticketing Integration**: Connect to incident management systems
- [ ] **Multi-tenant Setup**: Support for multiple CRPF sectors/regions
- [ ] **Custom Dashboard UI**: React-based frontend beyond Kibana
- [ ] **Blockchain Audit Trail**: Immutable log integrity verification
- [ ] **Alerting & Notifications**: Email/SMS alerts for critical events
- [ ] **Report Generation**: Automated daily/weekly security reports

---

## Documentation

| Document | Description |
|----------|-------------|
| [Problem Statement](docs/01_problem_statement.md) | SIH 1408 problem description and objectives |
| [System Requirements](docs/02_system_requirements.md) | Hardware, software, and network prerequisites |
| [Architecture](docs/03_architecture.md) | Detailed system architecture and data flow |
| [Deployment Guide](docs/04_deployment_guide.md) | Step-by-step installation instructions |
| [User Manual](docs/05_user_manual.md) | Role-based user guide with screenshots |
| [API Endpoints](docs/06_api_endpoints.md) | REST API documentation |
| [Troubleshooting](docs/07_troubleshooting.md) | Common issues and solutions |

---

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests for any enhancements.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Smart India Hackathon (SIH) 2023** - Problem Statement 1408
- **Elastic** - Elasticsearch, Logstash, Kibana
- **OpenSearch Project** - OpenSearch and Dashboards
- **Wazuh** - Open source security platform
- **Apache Kafka** - Distributed streaming platform
- **CRPF** - Central Reserve Police Force of India

---

## Contact

For questions or support regarding this project, please open an issue in the GitHub repository.

