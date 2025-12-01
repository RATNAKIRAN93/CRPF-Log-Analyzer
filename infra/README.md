# Infrastructure Configuration

This directory contains infrastructure-as-code and configuration files for deploying the CRPF Log Analyzer.

## Structure

```
infra/
├── docker-compose.yml      # Reference Docker Compose configuration
├── .env.example            # Environment variable template
├── metricbeat/             # Metricbeat agent configuration
│   └── metricbeat.yml.example
├── filebeat/               # Filebeat agent configuration
│   └── filebeat.yml.example
├── winlogbeat/             # Winlogbeat agent configuration
│   └── winlogbeat.yml.example
└── configs/                # Additional configuration files
```

## Quick Start

1. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your configuration:
   - Set server IP addresses
   - Configure passwords
   - Adjust memory settings

3. Deploy using Docker Compose:
   ```bash
   # From repository root
   docker compose up -d
   ```

## Agent Configuration

### Metricbeat (Linux System Metrics)

```bash
# Copy configuration
sudo cp metricbeat/metricbeat.yml.example /etc/metricbeat/metricbeat.yml

# Edit with your settings
sudo nano /etc/metricbeat/metricbeat.yml
# Replace <CENTRAL-SERVER-IP> with your server IP

# Start service
sudo systemctl enable metricbeat
sudo systemctl start metricbeat
```

### Filebeat (Linux Logs)

```bash
# Copy configuration
sudo cp filebeat/filebeat.yml.example /etc/filebeat/filebeat.yml

# Edit with your settings
sudo nano /etc/filebeat/filebeat.yml

# Enable modules
sudo filebeat modules enable system

# Start service
sudo systemctl enable filebeat
sudo systemctl start filebeat
```

### Winlogbeat (Windows Event Logs)

```powershell
# Copy configuration (run as Administrator)
Copy-Item winlogbeat\winlogbeat.yml.example "C:\Program Files\Winlogbeat\winlogbeat.yml"

# Edit configuration
notepad "C:\Program Files\Winlogbeat\winlogbeat.yml"
# Replace <CENTRAL-SERVER-IP> with your server IP

# Install and start service
cd "C:\Program Files\Winlogbeat"
.\install-service-winlogbeat.ps1
Start-Service winlogbeat
```

## Network Ports Reference

| Service | Port | Protocol |
|---------|------|----------|
| Elasticsearch/OpenSearch | 9200 | TCP |
| Kibana/OpenSearch Dashboards | 5601 | TCP |
| Logstash (Beats) | 5044 | TCP |
| Kafka | 9092 | TCP |
| Zookeeper | 2181 | TCP |
| FastAPI | 8000 | TCP |

## See Also

- [Deployment Guide](../docs/04_deployment_guide.md)
- [System Requirements](../docs/02_system_requirements.md)
- [Troubleshooting](../docs/07_troubleshooting.md)
