# Problem Statement

## SIH Problem Statement 1408: IT System Log Analyzer

**Domain**: Blockchain & Cybersecurity  
**Category**: Software  
**Organization**: Ministry of Home Affairs / CRPF

---

## Problem Description

The Central Reserve Police Force (CRPF) is one of the largest paramilitary forces in the world, with units and offices deployed across diverse locations throughout India. These units operate numerous IT systems including servers, workstations, network devices, and security appliances that generate vast amounts of log data daily.

### Current Challenges

1. **No Centralized Monitoring**: Each unit manages its own IT infrastructure independently with no unified view of system health or security posture

2. **Fragmented Log Storage**: Logs are stored locally at individual units, making cross-unit correlation and analysis impossible

3. **Delayed Threat Detection**: Without centralized monitoring, security breaches and threats often go undetected for extended periods

4. **Limited Expert Access**: Cybersecurity expertise is concentrated at headquarters, but they lack visibility into remote unit logs

5. **Difficult Forensics**: Building evidence for investigations requires manual collection of logs from multiple locations

6. **Resource Constraints**: Individual units lack the resources and expertise for comprehensive security monitoring

---

## Objective

Develop a **centralized IT system log analyzer** that enables CRPF cybersecurity experts to:

- Collect and aggregate logs from IT systems deployed at different CRPF locations
- Analyze logs in real-time for threat detection and anomaly identification
- Provide dashboards and reporting for security operations center (SOC) teams
- Enable forensic investigation and evidence building capabilities
- Scale to support multiple CRPF sectors and thousands of endpoints

---

## Constraints

| Constraint | Description |
|------------|-------------|
| **Network** | Must work across varied network conditions including low-bandwidth remote locations |
| **Security** | Must ensure secure transmission and storage of sensitive log data |
| **Scalability** | Must handle logs from thousands of endpoints across multiple sectors |
| **Compliance** | Must support audit requirements and evidence preservation |
| **Usability** | Must be accessible to users with varying technical expertise |
| **Cost** | Must use open-source technologies where possible to minimize costs |

---

## Success Criteria

### Functional Requirements

- [ ] Centralized collection of logs from Windows, Linux, and network devices
- [ ] Real-time log processing and indexing with sub-minute latency
- [ ] Rule-based threat detection for common attack patterns
- [ ] Anomaly detection using machine learning
- [ ] Role-based dashboards for different user types
- [ ] Search and query capabilities across all indexed logs
- [ ] Alert generation and notification for critical events
- [ ] Report generation for compliance and investigations

### Non-Functional Requirements

- [ ] System availability of 99.9%
- [ ] Log ingestion rate of 10,000+ events per second
- [ ] Search response time under 5 seconds for typical queries
- [ ] Data retention of 90+ days for compliance
- [ ] Secure transmission using TLS encryption
- [ ] Role-based access control with audit logging

---

## Target Users

| Role | Responsibilities | System Access |
|------|------------------|---------------|
| **SOC Analyst** | Monitor alerts, investigate incidents, triage threats | Full dashboard access, alert management |
| **System Administrator** | Manage infrastructure, configure agents, maintain system | System configuration, agent management |
| **Unit IT Officer** | Monitor unit-specific health, basic troubleshooting | Unit-scoped dashboards, limited search |
| **CRPF Cyber Cell** | Strategic oversight, compliance reporting, policy | Executive dashboards, reports |
| **Forensic Investigator** | Evidence collection, timeline reconstruction | Deep search, export capabilities |

---

## Expected Outcomes

1. **Reduced Detection Time**: From days/weeks to minutes/hours for security incidents
2. **Unified Visibility**: Single pane of glass for all CRPF IT infrastructure
3. **Improved Response**: Faster incident response through automated alerting
4. **Better Forensics**: Comprehensive log data for investigations
5. **Resource Optimization**: Centralized expertise serving all units
6. **Compliance Support**: Audit-ready logging and reporting

---

## References

- Smart India Hackathon 2023 - Problem Statement 1408
- CRPF IT Security Guidelines
- CERT-In Cybersecurity Best Practices
