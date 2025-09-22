#!/bin/bash

echo "🚀 Starting CRPF Log Analyzer Pipeline..."

# Step 1: Start infrastructure
echo "📋 Step 1: Starting infrastructure services..."
docker-compose up -d zookeeper
echo "⏳ Waiting for Zookeeper..."
sleep 10

docker-compose up -d kafka
echo "⏳ Waiting for Kafka..."
sleep 15

docker-compose up -d opensearch
echo "⏳ Waiting for OpenSearch..."
sleep 20

docker-compose up -d opensearch-dashboards kafka-ui
echo "⏳ Waiting for dashboards..."
sleep 10

# Step 2: Check service health
echo "🔍 Step 2: Checking service health..."

# Check Kafka
echo "Checking Kafka..."
docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Kafka is healthy"
else
    echo "❌ Kafka is not ready"
    exit 1
fi

# Check OpenSearch
echo "Checking OpenSearch..."
curl -s http://localhost:9200/_cluster/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ OpenSearch is healthy"
else
    echo "❌ OpenSearch is not ready"
    exit 1
fi

echo "🎉 All services are running!"
echo ""
echo "📊 Access Points:"
echo "  - OpenSearch Dashboards: http://localhost:5601"
echo "  - Kafka UI: http://localhost:8080"
echo "  - OpenSearch API: http://localhost:9200"
echo ""
echo "▶️  Next steps:"
echo "  1. Run: python services/kafka_to_opensearch.py"
echo "  2. Run: python services/enhanced_producer.py"
echo "  3. Open dashboards to view live data"
