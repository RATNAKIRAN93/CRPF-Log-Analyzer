import json
import time
import threading
import logging
from datetime import datetime, timezone
from kafka import KafkaProducer
from kafka.errors import KafkaError, NoBrokersAvailable, KafkaTimeoutError
import random
from faker import Faker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustKafkaProducer:
    def __init__(self, bootstrap_servers=['localhost:9092'], topic='crpf-logs'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None
        self.fake = Faker()
        self.max_retries = 10
        self.retry_backoff = 2  # seconds
        self.running = False
        
        # Producer configuration with retry settings
        self.producer_config = {
            'bootstrap_servers': self.bootstrap_servers,
            'retries': 10,  # Number of retries for failed sends
            'retry_backoff_ms': 1000,  # Wait time between retries
            'request_timeout_ms': 30000,  # Request timeout
            'delivery_timeout_ms': 120000,  # Total time for delivery
            'acks': 'all',  # Wait for all replicas
            'enable_idempotence': True,  # Prevent duplicates
            'max_in_flight_requests_per_connection': 1,  # Maintain order
            'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
            'key_serializer': lambda k: k.encode('utf-8') if k else None
        }

    def connect_with_retry(self):
        """Connect to Kafka with exponential backoff retry"""
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempting to connect to Kafka (attempt {attempt + 1}/{self.max_retries})")
                
                # Create producer with configuration
                self.producer = KafkaProducer(**self.producer_config)
                
                # Test connection by getting metadata
                metadata = self.producer.bootstrap_connected()
                if metadata:
                    logger.info("✅ Successfully connected to Kafka!")
                    return True
                    
            except NoBrokersAvailable:
                logger.warning(f"❌ No Kafka brokers available (attempt {attempt + 1})")
            except Exception as e:
                logger.error(f"❌ Connection error: {str(e)} (attempt {attempt + 1})")
            
            if attempt < self.max_retries - 1:
                wait_time = self.retry_backoff * (2 ** attempt)  # Exponential backoff
                logger.info(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
        
        logger.error("🚫 Failed to connect to Kafka after all retries")
        return False

    def generate_crpf_log(self, location_id: str):
        """Generate realistic CRPF log entry"""
        event_types = [
            'auth.login', 'auth.logout', 'auth.failed', 'file.access', 
            'process.start', 'process.stop', 'network.connection', 
            'security.alert', 'system.error', 'malware.detected'
        ]
        
        severity_levels = ['INFO', 'WARN', 'ERROR', 'CRITICAL']
        crpf_users = ['officer.kumar', 'inspector.sharma', 'constable.patel', 'admin.singh']
        
        # Generate suspicious patterns occasionally
        is_suspicious = random.random() < 0.1
        
        if is_suspicious:
            event_type = random.choice(['auth.failed', 'malware.detected', 'security.alert'])
            severity = random.choice(['ERROR', 'CRITICAL'])
        else:
            event_type = random.choice(event_types)
            severity = random.choices(severity_levels, weights=[60, 25, 10, 5])[0]
        
        log_entry = {
            '@timestamp': datetime.now(timezone.utc).isoformat(),
            'location_id': location_id,
            'host': f"crpf-{location_id}-{random.randint(1, 10)}",
            'event_type': event_type,
            'severity': severity,
            'user': random.choice(crpf_users),
            'source_ip': self.fake.ipv4_private(),
            'destination_ip': self.fake.ipv4() if random.random() > 0.7 else None,
            'message': self.fake.sentence(nb_words=8),
            'bytes_transferred': random.randint(100, 50000) if 'network' in event_type else None,
            'process_id': random.randint(1000, 9999) if 'process' in event_type else None
        }
        
        return log_entry

    def send_log(self, log_entry):
        """Send log entry to Kafka with error handling"""
        try:
            # Create key for partitioning (by location)
            key = log_entry['location_id']
            
            # Send to Kafka
            future = self.producer.send(
                self.topic, 
                value=log_entry, 
                key=key
            )
            
            # Add callback for success/failure
            future.add_callback(self.on_send_success)
            future.add_errback(self.on_send_error)
            
            return future
            
        except Exception as e:
            logger.error(f"❌ Failed to send log: {str(e)}")
            return None

    def on_send_success(self, record_metadata):
        """Callback for successful sends"""
        logger.debug(f"✅ Message sent to {record_metadata.topic} partition {record_metadata.partition}")

    def on_send_error(self, exception):
        """Callback for failed sends"""
        logger.error(f"❌ Failed to send message: {str(exception)}")

    def start_producing(self, location_ids, messages_per_second=5):
        """Start producing logs with specified rate"""
        if not self.connect_with_retry():
            logger.error("🚫 Cannot start producing - no Kafka connection")
            return
        
        self.running = True
        message_interval = 1.0 / messages_per_second
        
        logger.info(f"🚀 Starting log production for locations: {location_ids}")
        logger.info(f"📊 Rate: {messages_per_second} messages/second")
        
        try:
            while self.running:
                for location_id in location_ids:
                    if not self.running:
                        break
                        
                    log_entry = self.generate_crpf_log(location_id)
                    future = self.send_log(log_entry)
                    
                    if future:
                        logger.info(f"📤 Sent {log_entry['event_type']} from {location_id}")
                    
                    time.sleep(message_interval)
                    
        except KeyboardInterrupt:
            logger.info("⏹️  Production stopped by user")
        except Exception as e:
            logger.error(f"❌ Production error: {str(e)}")
        finally:
            self.stop_producing()

    def stop_producing(self):
        """Stop producing and cleanup"""
        self.running = False
        if self.producer:
            logger.info("🔄 Flushing remaining messages...")
            self.producer.flush(timeout=10)
            self.producer.close()
            logger.info("✅ Producer stopped and cleaned up")

def main():
    """Main function to start multiple producers"""
    # CRPF location IDs
    locations = [
        'delhi_hq', 'mumbai_west', 'kolkata_east', 
        'chennai_south', 'jammu_north', 'bhopal_central'
    ]
    
    # Create producer
    producer = RobustKafkaProducer(
        bootstrap_servers=['localhost:9092'],
        topic='crpf-logs'
    )
    
    # Start production with 2 messages per second
    producer.start_producing(locations, messages_per_second=2)

if __name__ == "__main__":
    main()
