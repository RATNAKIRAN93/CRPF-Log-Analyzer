import json
import time
from kafka import KafkaConsumer
from opensearchpy import OpenSearch, RequestsHttpConnection
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaToOpenSearchConsumer:
    def __init__(self):
        self.consumer = None
        self.opensearch = None
        self.running = False
        
    def connect_kafka(self):
        """Connect to Kafka consumer"""
        try:
            self.consumer = KafkaConsumer(
                'crpf-logs',
                bootstrap_servers=['localhost:9092'],
                auto_offset_reset='latest',
                enable_auto_commit=True,
                group_id='opensearch-indexer',
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            logger.info("✅ Connected to Kafka consumer")
            return True
        except Exception as e:
            logger.error(f"❌ Kafka connection failed: {e}")
            return False
    
    def connect_opensearch(self):
        """Connect to OpenSearch"""
        try:
            self.opensearch = OpenSearch(
                [{'host': 'localhost', 'port': 9200}],
                http_compress=True,
                use_ssl=False,
                verify_certs=False,
                connection_class=RequestsHttpConnection
            )
            
            # Test connection
            info = self.opensearch.info()
            logger.info(f"✅ Connected to OpenSearch: {info['version']['number']}")
            return True
        except Exception as e:
            logger.error(f"❌ OpenSearch connection failed: {e}")
            return False
    
    def create_index_template(self):
        """Create index template for CRPF logs"""
        template = {
            "index_patterns": ["crpf-logs-*"],
            "template": {
                "mappings": {
                    "properties": {
                        "@timestamp": {"type": "date"},
                        "location_id": {"type": "keyword"},
                        "host": {"type": "keyword"},
                        "event_type": {"type": "keyword"},
                        "severity": {"type": "keyword"},
                        "user": {"type": "keyword"},
                        "source_ip": {"type": "ip"},
                        "destination_ip": {"type": "ip"},
                        "message": {"type": "text"},
                        "bytes_transferred": {"type": "long"},
                        "process_id": {"type": "long"}
                    }
                },
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                }
            }
        }
        
        try:
            self.opensearch.indices.put_index_template(
                name="crpf-logs-template",
                body=template
            )
            logger.info("✅ Created OpenSearch index template")
        except Exception as e:
            logger.error(f"❌ Failed to create template: {e}")
    
    def start_consuming(self):
        """Start consuming from Kafka and indexing to OpenSearch"""
        if not self.connect_kafka() or not self.connect_opensearch():
            return
        
        self.create_index_template()
        self.running = True
        
        logger.info("🚀 Starting Kafka to OpenSearch pipeline")
        
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                log_data = message.value
                
                # Create daily index
                date_str = datetime.now().strftime('%Y.%m.%d')
                index_name = f"crpf-logs-{date_str}"
                
                try:
                    # Index to OpenSearch
                    response = self.opensearch.index(
                        index=index_name,
                        body=log_data
                    )
                    
                    logger.info(f"📥 Indexed: {log_data['event_type']} from {log_data['location_id']}")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to index message: {e}")
                    
        except KeyboardInterrupt:
            logger.info("⏹️  Consumer stopped by user")
        except Exception as e:
            logger.error(f"❌ Consumer error: {e}")
        finally:
            self.stop_consuming()
    
    def stop_consuming(self):
        """Stop consuming and cleanup"""
        self.running = False
        if self.consumer:
            self.consumer.close()
        logger.info("✅ Consumer stopped")

if __name__ == "__main__":
    consumer = KafkaToOpenSearchConsumer()
    consumer.start_consuming()
