# Placeholder Images

This directory contains SVG placeholder images for documentation purposes.

## Contents

| File | Description |
|------|-------------|
| `main_dashboard_placeholder.svg` | SOC dashboard mock-up |
| `discover_view_placeholder.svg` | OpenSearch Discover interface mock-up |
| `alert_details_placeholder.svg` | Alert investigation view mock-up |
| `system_health_placeholder.svg` | Infrastructure monitoring mock-up |

## Purpose

These placeholder images serve as:
- Documentation templates before actual screenshots are available
- Visual guides for what the actual screenshots should contain
- Reference designs for the expected UI layout

## Usage

To use in documentation while actual screenshots are pending:

```markdown
![Main Dashboard](examples/screenshots/placeholders/main_dashboard_placeholder.svg)
```

## Replacing Placeholders

Once the system is deployed and actual screenshots are captured:

1. Add real PNG screenshots to the parent `screenshots/` directory
2. Update README.md references to point to the actual images
3. Keep these placeholders for reference or remove them

## Note

These are SVG vector graphics that scale well for documentation but should be replaced with actual PNG screenshots for production documentation.
