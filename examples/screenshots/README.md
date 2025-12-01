# 📸 Screenshots

This directory contains screenshots of the CRPF Log Analyzer UI for documentation and training purposes.

---

## Required Screenshots

After deploying the CRPF Log Analyzer, capture the following screenshots:

| Screenshot | Description | What to Capture |
|------------|-------------|-----------------|
| `main_dashboard.png` | Primary SOC dashboard | Active alerts, log statistics, system health |
| `discover_view.png` | Log search interface | Search bar, time filter, log entries |
| `alert_details.png` | Alert investigation | Alert metadata, related events, timeline |
| `system_health.png` | Infrastructure monitoring | CPU, memory, disk metrics |
| `login_screen.png` | Login page (optional) | Authentication form |

---

## Screenshot Guidelines

### Technical Requirements
- **Resolution**: 1920x1080 or higher
- **Format**: PNG for best quality
- **Naming**: Use lowercase with underscores (e.g., `main_dashboard.png`)

### Content Guidelines
- **Redact sensitive information**: Remove or blur any real IP addresses, usernames, or classified data
- **Use sample data**: Ensure logs shown are from simulated producers, not real systems
- **Keep up-to-date**: Update screenshots when UI changes significantly

---

## How to Capture Screenshots

1. Start the CRPF Log Analyzer: `docker compose up -d`
2. Open OpenSearch Dashboards: http://localhost:5601
3. Navigate to the desired view
4. Use browser screenshot tool or:
   - **Windows**: Snipping Tool (Win+Shift+S)
   - **Linux**: gnome-screenshot, flameshot
   - **macOS**: Cmd+Shift+4

---

## Current Status

| Screenshot | Status |
|------------|--------|
| main_dashboard.png | ⏳ Pending |
| discover_view.png | ⏳ Pending |
| alert_details.png | ⏳ Pending |
| system_health.png | ⏳ Pending |

> **Note**: Screenshots will be added after deployment. The README.md currently uses sample Kibana documentation images.

---

## See Also

- [User Manual](../../docs/05_user_manual.md)
- [Dashboard Exports](../dashboards/)
