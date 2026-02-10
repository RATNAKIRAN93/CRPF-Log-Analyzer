# User Manual

This manual provides guidance for different user roles on how to use the CRPF Centralized IT System Log Analyzer effectively.

---

## User Roles

The system supports multiple user roles with different access levels and responsibilities:

| Role | Description | Access Level |
|------|-------------|--------------|
| **SOC Analyst** | Security Operations Center analyst responsible for monitoring alerts and investigating incidents | Full access to security dashboards, alerts, and search |
| **System Administrator** | Manages infrastructure, agents, and system configuration | System configuration, agent management, all indices |
| **Unit IT Officer** | IT staff at individual CRPF units, monitors local systems | Unit-scoped dashboards, limited search |
| **CRPF Cyber Cell** | Strategic oversight and compliance reporting | Executive dashboards, reports, read-only access |
| **Forensic Investigator** | Collects evidence and reconstructs attack timelines | Deep search, export capabilities, historical data |

---

## Getting Started

### Accessing the System

1. **OpenSearch Dashboards**: Navigate to `http://<server-ip>:5601`
2. **FastAPI**: Navigate to `http://<server-ip>:8000/docs`

### First Login

1. Open your web browser and navigate to the dashboard URL
2. Enter your credentials (provided by your administrator)
3. You will be directed to your role-specific home dashboard

---

## Dashboard Overview

### Main Dashboard Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CRPF Log Analyzer - Security Operations Dashboard                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Critical   │  │    High     │  │   Medium    │  │     Low     │        │
│  │     12      │  │     45      │  │    128      │  │    567      │        │
│  │   Alerts    │  │   Alerts    │  │   Alerts    │  │   Alerts    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Alert Timeline (Last 24 Hours)                   │   │
│  │  [═══════════════════════════════════════════════════════════════]  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌───────────────────────────┐  ┌───────────────────────────────────────┐  │
│  │     Top Alert Types       │  │          Recent Events                │  │
│  │  - Failed Login (34%)     │  │  10:45 - Failed SSH login             │  │
│  │  - File Modified (28%)    │  │  10:43 - Service started              │  │
│  │  - Process Started (18%)  │  │  10:42 - User created                 │  │
│  │  - Network Conn (12%)     │  │  10:40 - Config changed               │  │
│  │  - Other (8%)             │  │  10:38 - Failed login attempt         │  │
│  └───────────────────────────┘  └───────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Role-Specific Guides

### SOC Analyst Workflow

#### Daily Tasks

1. **Review Alert Summary**
   - Navigate to **Security Dashboard**
   - Check alert counts by severity
   - Focus on Critical and High alerts first

2. **Investigate Alerts**
   - Click on an alert to view details
   - Review related events
   - Check source endpoint information
   - Correlate with other alerts

3. **Search for Related Events**
   - Use the search bar or **Discover** view
   - Query example: `level:ERROR AND endpoint:server-001`
   - Expand time range to see historical context

4. **Document Findings**
   - Note investigation results
   - Update alert status (if ticketing integrated)
   - Escalate if necessary

#### Common Searches

| Purpose | Query Example |
|---------|---------------|
| Failed logins | `message:"Failed password" OR message:"Failed login"` |
| Specific user | `user:admin` |
| Specific endpoint | `endpoint:server-001` |
| Error events | `level:ERROR` |
| Time range | `@timestamp:[now-1h TO now]` |
| Combined | `level:ERROR AND user:admin AND endpoint:server-*` |

### System Administrator Workflow

#### Monitoring System Health

1. **Check Infrastructure Dashboard**
   - CPU, Memory, Disk usage across nodes
   - Elasticsearch cluster health
   - Agent connectivity status

2. **Verify Data Ingestion**
   - Navigate to **Discover**
   - Check recent event timestamps
   - Verify all expected indices are present

3. **Manage Agents**
   - Review agent heartbeats
   - Check for disconnected agents
   - Update agent configurations as needed

#### Administrative Tasks

```bash
# Check cluster health
curl -X GET "http://localhost:9200/_cluster/health?pretty"

# List indices
curl -X GET "http://localhost:9200/_cat/indices?v"

# Check agent status (example)
curl -X GET "http://localhost:8000/health"
```

### Unit IT Officer Workflow

#### Monitoring Your Unit

1. **Access Unit Dashboard**
   - Filter by your unit's endpoints
   - Review system health metrics
   - Check for local alerts

2. **Report Issues**
   - Identify anomalies in your unit
   - Escalate to SOC if security-related
   - Document for local remediation

#### Dashboard Filters

- Use the time picker to select date range
- Apply endpoint filters for your unit
- Save custom views for quick access

### Forensic Investigator Workflow

#### Evidence Collection

1. **Define Investigation Scope**
   - Time range of interest
   - Endpoints involved
   - Users of interest

2. **Search and Export**
   - Build comprehensive search queries
   - Review results in **Discover**
   - Export data for offline analysis

3. **Timeline Reconstruction**
   - Sort events chronologically
   - Correlate across multiple sources
   - Document chain of events

#### Export Data

1. Navigate to **Discover**
2. Run your search query
3. Click **Share** → **CSV Reports**
4. Download the exported data

---

## Using the Search Interface

### Basic Search

In the search bar, type your query:
- Simple text: `failed login`
- Field-specific: `user:admin`
- Wildcards: `endpoint:server-*`

### Advanced Search (Lucene Syntax)

| Operator | Example | Description |
|----------|---------|-------------|
| AND | `error AND admin` | Both terms must match |
| OR | `error OR warning` | Either term matches |
| NOT | `error NOT test` | Exclude term |
| "" | `"failed password"` | Exact phrase |
| * | `user:adm*` | Wildcard |
| ? | `user:admi?` | Single character wildcard |
| () | `(error OR warning) AND admin` | Grouping |
| [] | `status:[400 TO 500]` | Range |

### Saving Searches

1. Run your search query
2. Click **Save** in the toolbar
3. Enter a name for the saved search
4. Click **Save**

Access saved searches from the **Open** menu.

---

## Using Dashboards

### Navigating Dashboards

1. Click **Dashboard** in the left navigation
2. Select a dashboard from the list
3. Use the time picker to adjust the date range
4. Apply filters as needed

### Dashboard Interactions

- **Click** on a visualization to drill down
- **Hover** for detailed values
- **Filter** by clicking legend items
- **Zoom** on time-series charts by selecting a range

### Creating Custom Visualizations

1. Navigate to **Visualize**
2. Click **Create visualization**
3. Select visualization type (bar, line, pie, etc.)
4. Configure data source and aggregations
5. Save the visualization

### Adding to Dashboard

1. Open a dashboard in edit mode
2. Click **Add** → **Add from library**
3. Select your visualization
4. Arrange and resize as needed
5. Save the dashboard

---

## Alert Management

### Alert Severity Levels

| Level | Color | Response Time | Description |
|-------|-------|---------------|-------------|
| Critical | Red | Immediate | Active breach, data exfiltration |
| High | Orange | < 1 hour | Potential breach, suspicious activity |
| Medium | Yellow | < 4 hours | Anomalous behavior, policy violation |
| Low | Blue | < 24 hours | Informational, minor issues |

### Alert Triage Process

```
┌─────────────────┐
│  New Alert      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Review Details │
└────────┬────────┘
         │
    ┌────┴────┐
    │ Valid?  │
    └────┬────┘
         │
    ┌────┴────┬─── No ──▶ Mark False Positive
    │         │
   Yes        │
    │         │
    ▼         │
┌─────────────────┐
│  Investigate    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Take Action    │
│  - Contain      │
│  - Remediate    │
│  - Document     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Close Alert    │
└─────────────────┘
```

---

## Using the REST API

### Search Endpoint

```bash
# Basic search
curl "http://localhost:8000/search?q=level:ERROR"

# Search with specific fields
curl "http://localhost:8000/search?q=user:admin%20AND%20level:ERROR"
```

### Response Format

```json
{
  "count": 42,
  "results": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "endpoint": "server-001",
      "level": "ERROR",
      "message": "Failed password attempt",
      "user": "admin",
      "src_ip": "10.0.1.100"
    }
  ]
}
```

---

## Best Practices

### For All Users

- [ ] Review dashboards at the start of each shift
- [ ] Use specific time ranges to improve search performance
- [ ] Save frequently used searches for quick access
- [ ] Document investigation findings
- [ ] Report unusual activity immediately

### For SOC Analysts

- [ ] Prioritize Critical and High alerts
- [ ] Correlate alerts across multiple endpoints
- [ ] Check for patterns indicating coordinated attacks
- [ ] Maintain documentation for each investigation

### For System Administrators

- [ ] Monitor system resource utilization
- [ ] Regularly review agent connectivity
- [ ] Keep the system updated with security patches
- [ ] Backup configurations and important data

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `/` | Focus search bar |
| `Esc` | Close popup/modal |
| `Enter` | Execute search |
| `Ctrl+S` | Save current view |
| `R` | Refresh data |

---

## Getting Help

- **Documentation**: Review the docs folder in the repository
- **Troubleshooting**: See [07_troubleshooting.md](07_troubleshooting.md)
- **Support**: Contact your system administrator or raise an issue on GitHub
