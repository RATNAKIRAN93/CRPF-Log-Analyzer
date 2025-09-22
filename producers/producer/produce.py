import os
import time
import json
from kafka import KafkaProducer

# Read env vars
broker = os.getenv("KAFKA_BROKER", "kafka:9092")
endpoint = os.getenv("ENDPOINT_NAME", "default-endpoint")
topic = "system-logs"

# Retry until Kafka is up
producer = None
for i in range(10):
    try:
        producer = KafkaProducer(
            bootstrap_servers=[broker],
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        print(f"✅ Connected to Kafka at {broker}")
        break
    except Exception as e:
        print(f"Kafka not ready, retrying in 5s... ({e})")
        time.sleep(5)

if not producer:
    raise RuntimeError("❌ Could not connect to Kafka")

# Send logs continuously
i = 0
while True:
    msg = {"endpoint": endpoint, "msg": f"hello {i}"}
    producer.send(topic, value=msg)
    print(f"📤 Sent: {msg}")
    i += 1
    time.sleep(2)
