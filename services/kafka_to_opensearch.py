import json, time
from datetime import datetime
from kafka import KafkaConsumer
from opensearchpy import OpenSearch, RequestsHttpConnection

OS = OpenSearch(
    [{'host': 'localhost', 'port': 9200}],
    use_ssl=False, verify_certs=False,
    connection_class=RequestsHttpConnection, timeout=30
)

INDEX_TEMPLATE = {
  "index_patterns": ["crpf-logs-*"],
  "template": {
    "settings": {"number_of_shards": 1, "number_of_replicas": 0},
    "mappings": {
      "properties": {
        "@timestamp": {"type": "date"},
        "message": {"type": "text"},
        "log": {"properties": {"offset": {"type":"long"}, "file":{"properties":{"path":{"type":"keyword"}}}}},
        "host": {"properties": {"hostname":{"type":"keyword"}, "name":{"type":"keyword"}}},
        "container": {"properties": {"id":{"type":"keyword"}, "name":{"type":"keyword"}, "image":{"type":"keyword"}}},
        "stream": {"type":"keyword"},
        "crpf": {"properties": {"source":{"type":"keyword"}, "environment":{"type":"keyword"}}}
      }
    }
  }
}

def ensure_template():
    try:
        OS.indices.put_index_template(name="crpf-logs-template", body=INDEX_TEMPLATE)
    except Exception as e:
        print("template error:", e)

def index_record(doc):
    date = datetime.utcnow().strftime("%Y.%m.%d")
    idx = f"crpf-logs-{date}"
    try:
        OS.index(index=idx, body=doc)
    except Exception as e:
        print("index error:", e)

def main():
    ensure_template()
    consumer = KafkaConsumer(
        'crpf-endpoint-logs',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='crpf-opensearch-indexer',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')) if m and m[:1] in (b'{', b'[') else m
    )
    for msg in consumer:
        try:
            val = msg.value
            if isinstance(val, (bytes, str)):
                doc = {
                    "@timestamp": datetime.utcnow().isoformat(),
                    "message": val.decode() if isinstance(val, bytes) else val,
                    "stream": "raw"
                }
            else:
                # Filebeat JSON event
                doc = val
                if "@timestamp" not in doc:
                    doc["@timestamp"] = datetime.utcnow().isoformat()
            index_record(doc)
        except Exception as e:
            print("consume error:", e)

if __name__ == "__main__":
    main()
