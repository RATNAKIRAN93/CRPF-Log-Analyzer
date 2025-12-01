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

