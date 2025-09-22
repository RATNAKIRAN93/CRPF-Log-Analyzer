import os, json, time
from kafka import KafkaConsumer
from opensearchpy import OpenSearch

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "http://opensearch:9200")
INDEX = os.getenv("OPENSEARCH_INDEX", "system-logs")

consumer = KafkaConsumer(
    'system-logs',
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='log-indexer'
)

os_client = OpenSearch([OPENSEARCH_HOST], timeout=30)

# create index if not exists
try:
    if not os_client.indices.exists(INDEX):
        os_client.indices.create(index=INDEX, body={
            "settings": {"number_of_shards": 1, "number_of_replicas": 0}
        })
except Exception as e:
    print("Index setup error:", e)

print("Consumer started, consuming from Kafka and indexing to OpenSearch...")

for msg in consumer:
    doc = msg.value
    try:
        res = os_client.index(index=INDEX, document=doc)
        print("Indexed", res.get("_id"))
    except Exception as e:
        print("Indexing error:", e)
        time.sleep(1)
