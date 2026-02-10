# API Endpoints

This document describes the REST API endpoints provided by the CRPF Log Analyzer FastAPI backend service.

---

## Base URL

```
http://<server-ip>:8000
```

## Interactive Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: `http://<server-ip>:8000/docs`
- **ReDoc**: `http://<server-ip>:8000/redoc`

---

## Authentication

Currently, the API does not require authentication (development mode). For production deployments, implement one of the following:

- API Key authentication
- OAuth 2.0 / JWT tokens
- Basic authentication

---

## Endpoints

### Search Logs

Search for log events using Elasticsearch/OpenSearch query syntax.

**Endpoint**: `GET /search`

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | Search query using Elasticsearch query string syntax |

**Example Request**:

```bash
curl "http://localhost:8000/search?q=level:ERROR"
```

**Example Response**:

```json
{
  "count": 42,
  "results": [
    {
      "timestamp": "2024-01-15T10:30:00.000Z",
      "endpoint": "endpoint-1",
      "level": "ERROR",
      "message": "Failed password attempt",
      "user": "admin",
      "src_ip": "10.0.1.100",
      "dest_ip": "192.168.1.50",
      "pid": 1234
    },
    {
      "timestamp": "2024-01-15T10:29:45.000Z",
      "endpoint": "endpoint-2",
      "level": "ERROR",
      "message": "Service crashed",
      "user": "system",
      "src_ip": "10.0.2.50",
      "dest_ip": "192.168.2.100",
      "pid": 5678
    }
  ]
}
```

---

## Query Examples

### Search by Log Level

```bash
# All ERROR logs
curl "http://localhost:8000/search?q=level:ERROR"

# All WARN logs
curl "http://localhost:8000/search?q=level:WARN"

# Multiple levels
curl "http://localhost:8000/search?q=level:(ERROR%20OR%20WARN)"
```

### Search by Endpoint

```bash
# Specific endpoint
curl "http://localhost:8000/search?q=endpoint:endpoint-1"

# Wildcard endpoint search
curl "http://localhost:8000/search?q=endpoint:endpoint-*"
```

### Search by User

```bash
# Specific user
curl "http://localhost:8000/search?q=user:admin"

# Exclude system user
curl "http://localhost:8000/search?q=NOT%20user:system"
```

### Search by Message Content

```bash
# Exact phrase
curl "http://localhost:8000/search?q=message:%22Failed%20password%22"

# Contains word
curl "http://localhost:8000/search?q=message:*login*"
```

### Search by IP Address

```bash
# Source IP
curl "http://localhost:8000/search?q=src_ip:10.0.1.100"

# IP range (requires range query)
curl "http://localhost:8000/search?q=src_ip:10.0.1.*"
```

### Combined Queries

```bash
# ERROR logs from admin user
curl "http://localhost:8000/search?q=level:ERROR%20AND%20user:admin"

# Failed logins on specific endpoint
curl "http://localhost:8000/search?q=message:*Failed*%20AND%20endpoint:endpoint-1"

# All events from specific IP excluding INFO level
curl "http://localhost:8000/search?q=src_ip:10.0.1.100%20AND%20NOT%20level:INFO"
```

### Time-based Queries

```bash
# Note: Time-based queries require proper timestamp field syntax
curl "http://localhost:8000/search?q=timestamp:[2024-01-15T00:00:00Z%20TO%20*]"
```

---

## Response Format

### Success Response

```json
{
  "count": <number>,      // Total number of matching results
  "results": [            // Array of log documents
    {
      "timestamp": <string>,   // ISO 8601 timestamp
      "endpoint": <string>,    // Source endpoint name
      "level": <string>,       // Log level (INFO, WARN, ERROR, DEBUG)
      "message": <string>,     // Log message content
      "user": <string>,        // Associated user
      "src_ip": <string>,      // Source IP address
      "dest_ip": <string>,     // Destination IP address
      "pid": <number>          // Process ID
    }
  ]
}
```

### Error Response

```json
{
  "detail": "Error message describing the issue"
}
```

---

## Planned Endpoints

The following endpoints are planned for future releases:

### Health Check

```
GET /health
```

Returns the health status of the API and connected services.

**Planned Response**:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "services": {
    "opensearch": "connected",
    "kafka": "connected"
  }
}
```

### Get Alerts

```
GET /alerts
```

Retrieve security alerts filtered by severity, status, or time range.

**Planned Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `severity` | string | Filter by severity (critical, high, medium, low) |
| `status` | string | Filter by status (open, acknowledged, closed) |
| `from` | string | Start time (ISO 8601) |
| `to` | string | End time (ISO 8601) |
| `limit` | integer | Maximum results to return |

### Get Hosts

```
GET /hosts
```

List all monitored endpoints/hosts.

**Planned Response**:

```json
{
  "count": 10,
  "hosts": [
    {
      "name": "endpoint-1",
      "ip": "10.0.1.100",
      "os": "Linux",
      "last_seen": "2024-01-15T10:30:00.000Z",
      "status": "active",
      "agents": ["filebeat", "metricbeat"]
    }
  ]
}
```

### Get Host Details

```
GET /hosts/{hostname}
```

Get detailed information about a specific host.

### Get Statistics

```
GET /stats
```

Get aggregate statistics about log data.

**Planned Response**:

```json
{
  "total_events": 1000000,
  "events_24h": 50000,
  "events_by_level": {
    "INFO": 35000,
    "WARN": 10000,
    "ERROR": 4500,
    "DEBUG": 500
  },
  "top_endpoints": [
    {"name": "endpoint-1", "count": 15000},
    {"name": "endpoint-2", "count": 12000}
  ],
  "top_users": [
    {"name": "system", "count": 20000},
    {"name": "admin", "count": 5000}
  ]
}
```

### Export Data

```
POST /export
```

Export search results in various formats.

**Planned Request Body**:

```json
{
  "query": "level:ERROR AND user:admin",
  "from": "2024-01-14T00:00:00Z",
  "to": "2024-01-15T00:00:00Z",
  "format": "csv",
  "fields": ["timestamp", "endpoint", "level", "message", "user"]
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production deployments, consider implementing:

- Request rate limiting (e.g., 100 requests per minute)
- Result size limits
- Query complexity limits

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid query syntax |
| 401 | Unauthorized - Invalid or missing credentials |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource does not exist |
| 500 | Internal Server Error - OpenSearch or service error |
| 503 | Service Unavailable - Backend service unavailable |

---

## SDK Examples

### Python

```python
import requests

# Search for error logs
response = requests.get(
    "http://localhost:8000/search",
    params={"q": "level:ERROR"}
)

data = response.json()
print(f"Found {data['count']} results")

for log in data['results']:
    print(f"{log['timestamp']} - {log['endpoint']}: {log['message']}")
```

### JavaScript

```javascript
// Using fetch API
async function searchLogs(query) {
    const response = await fetch(
        `http://localhost:8000/search?q=${encodeURIComponent(query)}`
    );
    const data = await response.json();
    console.log(`Found ${data.count} results`);
    return data.results;
}

// Example usage
searchLogs('level:ERROR AND user:admin')
    .then(results => results.forEach(log => 
        console.log(`${log.timestamp} - ${log.endpoint}: ${log.message}`)
    ));
```

### cURL

```bash
# Search with output formatting
curl -s "http://localhost:8000/search?q=level:ERROR" | jq '.results[] | "\(.timestamp) - \(.endpoint): \(.message)"'
```

---

## OpenAPI Specification

The full OpenAPI specification is available at:

```
http://localhost:8000/openapi.json
```

This can be imported into API testing tools like Postman or Insomnia.
