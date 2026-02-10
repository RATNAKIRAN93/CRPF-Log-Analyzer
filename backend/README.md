# Backend Services

This directory contains the backend API and automation scripts for the CRPF Log Analyzer.

## Structure

```
backend/
├── api/              # REST API services
└── scripts/          # Automation and setup scripts
```

## API Services

The main FastAPI service is located in `/fastapi` directory at the repository root. Future backend services and API enhancements will be developed here.

### Planned Services

- **Alert Management API**: CRUD operations for security alerts
- **Asset Management API**: Endpoint inventory and status
- **Reporting API**: Generate compliance and incident reports
- **Integration API**: Connect with ticketing systems

## Scripts

Place automation and setup scripts here:

- Index management scripts
- Agent deployment scripts
- Backup and restore scripts
- Data migration scripts

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run API locally
uvicorn main:app --reload --port 8000
```

## See Also

- [API Endpoints Documentation](../docs/06_api_endpoints.md)
- [Main FastAPI Service](../fastapi/)
