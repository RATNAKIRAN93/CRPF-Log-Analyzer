# Additional Configuration Files

This directory contains additional configuration files for the CRPF Log Analyzer infrastructure.

## Contents

Store configuration files here:

- Logstash pipeline configurations
- Elasticsearch index templates
- Wazuh rules and decoders
- NGINX reverse proxy config
- SSL/TLS certificates (gitignored)

## Logstash Pipelines

Example pipeline configurations for different log sources:

```conf
# Example: /etc/logstash/conf.d/beats.conf
input {
  beats {
    port => 5044
  }
}

filter {
  # Add your filters here
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "%{[@metadata][beat]}-%{+YYYY.MM.dd}"
  }
}
```

## Index Templates

Custom index templates for optimizing log storage and search.

## Security Notes

⚠️ Do not commit sensitive files:
- SSL certificates and keys
- API tokens
- Passwords

Add sensitive files to `.gitignore`.
