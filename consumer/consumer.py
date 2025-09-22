import os
import json
import time
from kafka import KafkaConsumer
from opensearchpy import OpenSearch

# Env vars
broker = os.getenv("KAFKA_BROKER", "kafka:9092")
os_host = os.getenv("OPENSEARCH_HOST", "http://opensearch:9200")
index = os.getenv("OPENSEARCH_INDEX", "system-logs")

# Retry until Kafka is up
consumer = None
for i in range(10):
    try:
        consumer = KafkaConsumer(
            "system-logs",
            bootstrap_servers=[broker],
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="log-analyzer-group"
        )
        print(f"✅ Connected to Kafka at {broker}")
        break
    except Exception as e:
        print(f"Kafka not ready, retrying in 5s... ({e})")
        time.sleep(5)

if not consumer:
    raise RuntimeError("❌ Could not connect to Kafka")

# Connect to OpenSearch
client = OpenSearch([os_host])
if not client.indices.exists(index=index):
    client.indices.create(index=index)

# Consume and index
for msg in consumer:
    doc = msg.value
    res = client.index(index=index, body=doc)
    print(f"📥 Indexed into OpenSearch: {res['_id']} -> {doc}")
