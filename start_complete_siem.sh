#!/bin/bash

echo "🚀 Starting Complete CRPF SIEM System..."

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Activated virtual environment"
fi

# Start infrastructure
echo "📋 Starting infrastructure services..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Test Kafka
docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Kafka is ready"
else
    echo "❌ Kafka not ready"
    exit 1
fi

# Test OpenSearch
curl -s http://localhost:9200/_cluster/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ OpenSearch is ready"
else
    echo "❌ OpenSearch not ready"
    exit 1
fi

echo ""
echo "🎉 Infrastructure is ready!"
echo ""
echo "📊 Service Access Points:"
echo "  - OpenSearch Dashboards: http://localhost:5601"
echo "  - Kafka UI: http://localhost:8080" 
echo "  - OpenSearch API: http://localhost:9200"
echo ""
echo "🚀 Starting CRPF SIEM Services..."
echo ""
echo "Run these commands in separate terminals:"
echo ""
echo "Terminal 1 - Data Pipeline:"
echo "  python services/kafka_to_opensearch.py"
echo ""
echo "Terminal 2 - Realistic Log Generator:"
echo "  python services/crpf_realistic_producer.py"
echo ""
echo "Terminal 3 - Alert Manager:"
echo "  python services/crpf_alert_manager.py"
echo ""
echo "Terminal 4 - Security Dashboard:"
echo "  streamlit run dashboard/crpf_security_dashboard.py --server.port 8501 --server.address 0.0.0.0"
echo ""
echo "🛡️ CRPF SIEM System Ready for Operation!"
