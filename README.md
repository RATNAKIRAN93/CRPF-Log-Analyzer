# CRPF-Log-Analyzer

CRPF units/offices and personnel are deployed in different location of CRPF. There is no centralised system to analyse the log of IT system by the experts to access threats and breaches. 

## Proposed Solution
Centralized system should be developed for analysing the systems deployed at the different location of the country. This system integrates multiple security monitoring tools including Wazuh for comprehensive log analysis and threat detection.

## Features
- **Centralized Log Analysis**: Collect and analyze logs from multiple CRPF locations
- **Wazuh Integration**: Enterprise-grade security monitoring and threat detection
- **Real-time Monitoring**: Live dashboards for security event monitoring
- **Alert Management**: Automated alerting for security incidents
- **Scalable Architecture**: Docker-based infrastructure for easy deployment

## Installation

### 1. CRPF Log Analyzer Infrastructure
```bash
# Start the main CRPF pipeline
./start_crpf_pipeline.sh

# Or start the complete SIEM system
./start_complete_siem.sh
```

### 2. Wazuh Security Platform Installation
Install Wazuh in all-in-one mode for comprehensive security monitoring:

```bash
# Download and install Wazuh (requires root privileges)
sudo ./install_wazuh.sh
```

This will:
- Download the official Wazuh installation script from https://packages.wazuh.com/4.13/wazuh-install.sh
- Install Wazuh Manager, Indexer, and Dashboard in all-in-one mode
- Configure services and provide access information
- Create configuration backups

**Default Wazuh Access:**
- URL: https://localhost:443
- Username: admin
- Password: admin (change immediately after first login)

### 3. Service Access Points
- **OpenSearch Dashboards**: http://localhost:5601
- **Kafka UI**: http://localhost:8080
- **Wazuh Dashboard**: https://localhost:443
- **Security Dashboard**: http://localhost:8501

## Architecture
The system uses a modern, scalable architecture:
- **Kafka**: Message streaming for log data
- **OpenSearch**: Log storage and search
- **Wazuh**: Security monitoring and threat detection
- **Docker**: Containerized services for easy deployment
- **Python Services**: Log processing and alert management

## Security Notes
⚠️ **Important**: After installation, immediately:
1. Change default Wazuh admin password
2. Configure SSL certificates for production
3. Review and configure firewall rules
4. Set up proper network security between CRPF locations
