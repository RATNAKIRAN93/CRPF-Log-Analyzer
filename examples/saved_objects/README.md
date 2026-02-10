# Saved Objects

This directory contains exported Kibana/OpenSearch Dashboards saved objects.

## Contents

Export and store your saved objects here:

- `index_patterns.ndjson` - Index pattern definitions
- `searches.ndjson` - Saved searches
- `visualizations.ndjson` - Visualizations
- `dashboards.ndjson` - Dashboard configurations

## Exporting Saved Objects

1. Open Kibana/OpenSearch Dashboards
2. Navigate to **Stack Management** → **Saved Objects**
3. Select objects to export
4. Click **Export**
5. Save the NDJSON file to this directory

## Importing Saved Objects

1. Open Kibana/OpenSearch Dashboards
2. Navigate to **Stack Management** → **Saved Objects**
3. Click **Import**
4. Select the NDJSON file
5. Resolve any conflicts
6. Click **Import**

## Best Practices

- Export objects after significant dashboard changes
- Include in version control for backup
- Document what each export contains
- Test imports in a staging environment first
