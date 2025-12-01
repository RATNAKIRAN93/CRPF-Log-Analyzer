# Frontend Dashboard UI

This directory is reserved for custom frontend dashboard development beyond Kibana/OpenSearch Dashboards.

## Structure

```
frontend/
└── dashboard-ui/     # React/Vite custom dashboard application
```

## Current Status

The primary visualization interface is provided by:
- **OpenSearch Dashboards**: http://localhost:5601
- **Kibana** (ELK stack): http://localhost:5601

## Planned Development

A custom React-based dashboard is planned to provide:

- Simplified SOC analyst interface
- CRPF-branded user experience
- Integration with Kibana/OpenSearch via iframes
- Custom alert management workflows
- Role-specific views (SOC, Admin, Unit IT Officer)

## Technology Stack

- **React 18+**: UI framework
- **Vite**: Build tool
- **Material-UI** or **Ant Design**: Component library
- **React Query**: Data fetching and caching
- **React Router**: Navigation

## Getting Started (Future)

```bash
cd frontend/dashboard-ui

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## See Also

- [User Manual](../docs/05_user_manual.md)
- [API Endpoints](../docs/06_api_endpoints.md)
