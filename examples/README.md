# Examples

This directory contains sample data, exported dashboards, and screenshots for the CRPF Log Analyzer.

## Structure

```
examples/
├── sample_logs/       # Example log files for testing
├── saved_objects/     # Exported Kibana/OpenSearch saved objects
├── dashboards/        # Dashboard JSON exports
└── screenshots/       # UI screenshots for documentation
```

## Sample Logs

Example log files demonstrating different log formats and events:
- Windows Security Event logs
- Linux syslog/auth logs
- Application error logs
- Simulated attack patterns

## Saved Objects

Exported Kibana/OpenSearch Dashboards saved objects that can be imported:
- Index patterns
- Saved searches
- Visualizations
- Dashboards

### Importing Saved Objects

1. Open Kibana/OpenSearch Dashboards
2. Navigate to **Stack Management** → **Saved Objects**
3. Click **Import**
4. Select the NDJSON file from `saved_objects/`
5. Click **Import**

## Dashboards

Pre-built dashboard configurations:
- Security Operations Dashboard
- System Health Dashboard
- Alert Summary Dashboard
- Investigation Dashboard

## Screenshots

UI screenshots for documentation and training:
- Login screen
- Main dashboard
- Alert investigation workflow
- Search interface

## Usage

These examples are provided for:
- Testing and validation
- Training and onboarding
- Documentation reference
- Demonstration purposes

## Contributing

To add new examples:
1. Export from Kibana/OpenSearch Dashboards
2. Place files in appropriate subdirectory
3. Update this README with descriptions
