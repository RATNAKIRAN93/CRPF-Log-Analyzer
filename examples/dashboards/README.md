# Dashboard Exports

This directory contains exported dashboard configurations in JSON format.

## Available Dashboards

Store dashboard JSON exports here:

- Security Operations Dashboard
- System Health Overview
- Alert Summary Dashboard
- Endpoint Monitoring Dashboard
- Investigation Workspace

## Format

Dashboards are exported as NDJSON (Newline Delimited JSON) files from Kibana/OpenSearch Dashboards.

## Usage

Import these dashboards to quickly set up your visualization environment:

```bash
# Using Kibana API
curl -X POST "http://localhost:5601/api/saved_objects/_import" \
  -H "kbn-xsrf: true" \
  --form file=@security_dashboard.ndjson
```

Or import via the UI:
1. Stack Management → Saved Objects → Import
