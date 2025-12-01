# Sample Log Files

This directory contains sample log data for testing and demonstration purposes.

## Files

Place sample log files here in various formats:

- `sample_windows_security.json` - Windows Security Event logs
- `sample_linux_auth.log` - Linux authentication logs
- `sample_syslog.log` - Syslog format messages
- `sample_alerts.json` - Security alert examples

## Usage

These logs can be used for:
- Testing log parsing configurations
- Validating index patterns
- Training and demonstrations
- Developing new detection rules

## Generating Test Data

The simulated producers in `/producers` directory generate test data automatically when running the Docker Compose stack.

To generate additional test data, run:

```bash
# Start producers only
docker compose up -d producer1 producer2
```
