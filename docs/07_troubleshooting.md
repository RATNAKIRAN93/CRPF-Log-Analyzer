# Troubleshooting Guide

This guide covers common issues encountered when deploying and operating the CRPF Centralized IT System Log Analyzer, along with their solutions.

---

## Quick Diagnostics

Before diving into specific issues, run these diagnostic commands:

```bash
# Check all container status
docker compose ps

# Check container logs (replace <service> with service name)
docker compose logs <service>

# Check system resources
free -h
df -h
docker stats --no-stream

# Check network connectivity
curl -s http://localhost:9200/_cluster/health?pretty
curl -s http://localhost:5601/api/status
```

---

## Common Issues

### 1. Elasticsearch/OpenSearch Won't Start

**Symptoms**:
- Container exits immediately
- "max virtual memory areas vm.max_map_count is too low" error

**Solution**:

```bash
# Increase vm.max_map_count (required for Elasticsearch)
sudo sysctl -w vm.max_map_count=262144

# Make persistent across reboots
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

---

### 2. Elasticsearch Authentication Error (401)

**Symptoms**:
- "401 Unauthorized" when accessing Elasticsearch
- Beats/Logstash failing to connect

**Solution**:

```bash
# For ELK stack, ensure passwords are set correctly
cd docker-elk
cat .env | grep PASSWORD

# Re-run setup to reset passwords
docker compose --profile setup up setup

# Verify with curl
curl -u elastic:changeme http://localhost:9200/_cluster/health
```

For Beats configuration, ensure credentials match:

```yaml
output.elasticsearch:
  hosts: ["localhost:9200"]
  username: "elastic"
  password: "your-password"
```

---

### 3. Kibana/OpenSearch Dashboards Not Accessible

**Symptoms**:
- Cannot reach http://localhost:5601
- "Connection refused" error

**Solution**:

```bash
# Check if container is running
docker compose ps kibana   # or opensearch-dashboards

# Check container logs
docker compose logs kibana

# Verify port binding
sudo netstat -tlnp | grep 5601

# If behind firewall, open the port
sudo ufw allow 5601/tcp
```

Wait 2-3 minutes after starting - Kibana takes time to initialize.

---

### 4. Metricbeat Connection Errors

**Symptoms**:
- "connection refused" to Elasticsearch
- "Kibana setup failed" error

**Solution**:

```bash
# Test Elasticsearch connectivity from Metricbeat host
curl -u elastic:password http://<elasticsearch-ip>:9200

# Check Metricbeat configuration
sudo metricbeat test config
sudo metricbeat test output

# Common config issues - verify /etc/metricbeat/metricbeat.yml
output.elasticsearch:
  hosts: ["<correct-ip>:9200"]
  username: "elastic"
  password: "<correct-password>"

setup.kibana:
  host: "<correct-ip>:5601"
  username: "elastic"
  password: "<correct-password>"
```

---

### 5. Beats Not Sending Data

**Symptoms**:
- No data appearing in Elasticsearch
- Agent appears to be running but no events indexed

**Solution**:

```bash
# Check Beat service status
sudo systemctl status metricbeat  # or filebeat, winlogbeat

# View Beat logs
sudo journalctl -u metricbeat -f

# Test Beat configuration
sudo metricbeat test config -e
sudo metricbeat test output -e

# Manually run Beat in foreground for debugging
sudo metricbeat -e -v
```

Common causes:
- Incorrect Elasticsearch URL
- Firewall blocking port 9200
- Wrong credentials
- Index template not loaded

---

### 6. Kafka Connection Issues

**Symptoms**:
- Producers/consumers can't connect to Kafka
- "Connection refused" to port 9092

**Solution**:

```bash
# Check Kafka and Zookeeper status
docker compose ps kafka zookeeper

# View Kafka logs
docker compose logs kafka

# Verify Kafka is listening
docker compose exec kafka kafka-topics.sh --list --bootstrap-server localhost:9092

# Check advertised listeners in docker-compose.yml
# Ensure KAFKA_ADVERTISED_LISTENERS is correctly configured
```

For external access, update Kafka configuration:

```yaml
environment:
  - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092,EXTERNAL://<host-ip>:9093
  - KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,EXTERNAL:PLAINTEXT
```

---

### 7. Port 5601 Not Reachable from External Host

**Symptoms**:
- Kibana works on localhost but not from other machines
- Timeout when accessing from browser

**Solution**:

```bash
# Check if Kibana is binding to all interfaces
docker compose exec kibana cat /usr/share/kibana/config/kibana.yml | grep server.host

# Should be:
server.host: "0.0.0.0"

# Check firewall
sudo ufw status
sudo ufw allow 5601/tcp

# Check if Docker is using correct network
docker network inspect crpf-log-analyzer_default
```

---

### 8. Out of Disk Space

**Symptoms**:
- Elasticsearch cluster goes to red status
- "No space left on device" errors

**Solution**:

```bash
# Check disk usage
df -h
docker system df

# Clean up Docker resources
docker system prune -a --volumes  # WARNING: This removes unused data!

# Clean up old indices (use with caution)
# Delete indices older than 30 days
curl -X DELETE "localhost:9200/system-logs-2024.01.*"

# Set up index lifecycle management (ILM) to auto-delete old data
```

Configure ILM in Kibana:
1. Go to Stack Management → Index Lifecycle Policies
2. Create a policy with delete phase after X days
3. Apply to index template

---

### 9. High Memory Usage

**Symptoms**:
- System becomes slow
- Elasticsearch/Kibana OOM killed

**Solution**:

```bash
# Check current memory usage
free -h
docker stats

# Reduce Elasticsearch heap size in docker-compose.yml
environment:
  - ES_JAVA_OPTS=-Xms512m -Xmx512m  # Adjust based on available RAM

# Reduce Logstash heap if using
environment:
  - LS_JAVA_OPTS=-Xms256m -Xmx256m

# Restart services
docker compose restart elasticsearch logstash
```

Memory allocation guidelines:
- Elasticsearch: 50% of available RAM, max 32 GB
- Reserve at least 2-4 GB for OS and other services

---

### 10. Slow Search Performance

**Symptoms**:
- Searches taking more than 5-10 seconds
- Dashboard loading slowly

**Solution**:

```bash
# Check cluster health
curl -s localhost:9200/_cluster/health?pretty

# Check index size
curl -s localhost:9200/_cat/indices?v

# Check for unassigned shards
curl -s localhost:9200/_cat/shards?h=index,shard,prirep,state,unassigned.reason | grep UNASSIGNED
```

Optimizations:
- Increase refresh interval for write-heavy indices
- Use appropriate number of shards (1 shard per 50 GB)
- Implement hot-warm architecture for older data
- Add more Elasticsearch nodes for large deployments

---

### 11. Windows Winlogbeat Issues

**Symptoms**:
- Winlogbeat service won't start
- Permission denied errors

**Solution** (run PowerShell as Administrator):

```powershell
# Check service status
Get-Service winlogbeat

# View Windows Event Log for Winlogbeat errors
Get-EventLog -LogName Application -Source Winlogbeat -Newest 10

# Test configuration
cd "C:\Program Files\Winlogbeat"
.\winlogbeat.exe test config -e

# Reinstall service
.\uninstall-service-winlogbeat.ps1
.\install-service-winlogbeat.ps1

# Start service
Start-Service winlogbeat
```

Common Windows issues:
- Run PowerShell as Administrator
- Check Windows Firewall allows outbound port 9200
- Ensure correct line endings in YAML file (use LF, not CRLF)

---

### 12. Index Pattern Creation Fails

**Symptoms**:
- "No results found" when creating index pattern
- Index pattern doesn't show any fields

**Solution**:

1. Verify data exists in Elasticsearch:
```bash
curl -s "localhost:9200/_cat/indices?v" | grep system-logs
```

2. Check if index has documents:
```bash
curl -s "localhost:9200/system-logs/_count"
```

3. If no data, check:
   - Producers are running: `docker compose ps producer1 producer2`
   - Consumer is running: `docker compose ps consumer`
   - Consumer logs: `docker compose logs consumer`

4. Refresh index pattern:
   - In Kibana/OpenSearch Dashboards
   - Go to Stack Management → Index Patterns
   - Select your pattern and click "Refresh field list"

---

### 13. SSL/TLS Certificate Errors

**Symptoms**:
- "certificate verify failed" errors
- Beats can't connect with HTTPS

**Solution**:

For self-signed certificates:

```yaml
# In Beat configuration
output.elasticsearch:
  hosts: ["https://localhost:9200"]
  ssl.verification_mode: none  # Only for testing!

# Better: Trust the CA certificate
output.elasticsearch:
  hosts: ["https://localhost:9200"]
  ssl.certificate_authorities: ["/path/to/ca.crt"]
```

---

## Diagnostic Commands Reference

### Docker Commands

```bash
# View all containers
docker compose ps -a

# View logs for specific service
docker compose logs -f <service-name>

# Enter container shell
docker compose exec <service-name> bash

# Restart specific service
docker compose restart <service-name>

# View resource usage
docker stats
```

### Elasticsearch Commands

```bash
# Cluster health
curl -s localhost:9200/_cluster/health?pretty

# Node info
curl -s localhost:9200/_nodes/stats?pretty

# Index stats
curl -s localhost:9200/_cat/indices?v

# Shard allocation
curl -s localhost:9200/_cat/shards?v

# Pending tasks
curl -s localhost:9200/_cluster/pending_tasks?pretty
```

### Kafka Commands

```bash
# List topics
docker compose exec kafka kafka-topics.sh --list --bootstrap-server localhost:9092

# Describe topic
docker compose exec kafka kafka-topics.sh --describe --topic system-logs --bootstrap-server localhost:9092

# View consumer groups
docker compose exec kafka kafka-consumer-groups.sh --list --bootstrap-server localhost:9092
```

---

## Getting Further Help

If you continue to experience issues:

1. **Check Logs**: Always start by reviewing container logs
2. **Search Issues**: Check GitHub Issues for similar problems
3. **Documentation**: Review official documentation for Elasticsearch, Kibana, Kafka
4. **Community**: Ask on Elastic forums or Stack Overflow
5. **File Issue**: Create a detailed GitHub issue with:
   - Error messages
   - Log outputs
   - System specifications
   - Steps to reproduce
