# Screenshots

This directory contains screenshots of the CRPF Log Analyzer UI for documentation and training purposes.

---

## Required Screenshots

Add the following screenshots to complete the documentation:

### 1. **main_dashboard.png**
- **Description**: Primary SOC dashboard
- **What to capture**: Main security monitoring dashboard after login
- **Should show**: Active alerts, log statistics, system health metrics, recent events

### 2. **discover_view.png**
- **Description**: Log search interface
- **What to capture**: OpenSearch Dashboards Discover tab
- **Should show**: Search bar, time filter, log entries, field sidebar

### 3. **alert_details.png**
- **Description**: Alert investigation view
- **What to capture**: Detailed view of a security alert
- **Should show**: Alert metadata, related events, timeline, actions

### 4. **system_health.png**
- **Description**: Infrastructure monitoring
- **What to capture**: System health dashboard
- **Should show**: CPU, memory, disk metrics, endpoint status

### 5. **login_screen.png** (optional)
- **Description**: Login/authentication page
- **What to capture**: Login form before authentication
- **Should show**: Username/password fields, CRPF branding

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

### Using Browser
1. Start the CRPF Log Analyzer stack: `docker compose up -d`
2. Open OpenSearch Dashboards: http://localhost:5601
3. Navigate to the desired view
4. Use browser screenshot tool (F12 → Device toolbar → Capture screenshot)

### Using Tools
- **Windows**: Snipping Tool (Win+Shift+S)
- **Linux**: gnome-screenshot, flameshot
- **macOS**: Cmd+Shift+4

### Full Page Capture
For scrolling pages, use browser extensions:
- Chrome: "Full Page Screen Capture"
- Firefox: Built-in (Ctrl+Shift+S)

---

## Usage in Documentation

Reference screenshots in markdown files:

```markdown
![Main Dashboard](examples/screenshots/main_dashboard.png)
*Description of what the screenshot shows*

![Discover View](examples/screenshots/discover_view.png)
*Log search and discovery interface*
```

---

## Current Status

| Screenshot | Status | Notes |
|------------|--------|-------|
| main_dashboard.png | ⏳ Pending | Add after initial deployment |
| discover_view.png | ⏳ Pending | Capture from OpenSearch Dashboards |
| alert_details.png | ⏳ Pending | Create sample alert first |
| system_health.png | ⏳ Pending | Requires Metricbeat data |
| login_screen.png | ⏳ Pending | Optional |

---

## See Also

- [User Manual](../../docs/05_user_manual.md) - Uses these screenshots
- [Dashboard Exports](../dashboards/) - Kibana/OpenSearch dashboard JSON files
