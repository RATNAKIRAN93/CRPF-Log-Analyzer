import json
import time
import requests
import logging
from datetime import datetime, timedelta
from kafka import KafkaConsumer
import threading
from collections import defaultdict, deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CRPFAlertManager:
    def __init__(self):
        self.opensearch_url = "http://localhost:9200"
        self.consumer = None
        self.running = False
        
        # Alert rules configuration
        self.alert_rules = {
            'brute_force_detection': {
                'description': 'Multiple failed login attempts',
                'condition': 'event_type:login_failed',
                'threshold': 5,
                'time_window': 300,  # 5 minutes
                'severity': 'HIGH'
            },
            'malware_detection': {
                'description': 'Malware detected on endpoint',
                'condition': 'event_type:malware_detected',
                'threshold': 1,
                'time_window': 60,
                'severity': 'CRITICAL'
            },
            'high_risk_activity': {
                'description': 'High risk score events',
                'condition': 'risk_score>=80',
                'threshold': 3,
                'time_window': 600,  # 10 minutes
                'severity': 'HIGH'
            },
            'intrusion_attempt': {
                'description': 'Intrusion attempts detected',
                'condition': 'event_type:intrusion_attempt',
                'threshold': 1,
                'time_window': 60,
                'severity': 'CRITICAL'
            },
            'insider_threat': {
                'description': 'Potential insider threat activity',
                'condition': 'threat_level:malicious AND event_category:security',
                'threshold': 2,
                'time_window': 1800,  # 30 minutes
                'severity': 'CRITICAL'
            }
        }
        
        # Event buffers for time-based analysis
        self.event_buffers = defaultdict(lambda: deque(maxlen=1000))
        self.active_alerts = {}

    def connect_kafka(self):
        """Connect to Kafka consumer"""
        try:
            self.consumer = KafkaConsumer(
                'crpf-logs',
                bootstrap_servers=['localhost:9092'],
                auto_offset_reset='latest',
                group_id='alert-manager',
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            logger.info("✅ Connected to Kafka for alert monitoring")
            return True
        except Exception as e:
            logger.error(f"❌ Kafka connection failed: {e}")
            return False

    def create_alert_index(self):
        """Create OpenSearch index for alerts"""
        alert_mapping = {
            "mappings": {
                "properties": {
                    "@timestamp": {"type": "date"},
                    "alert_id": {"type": "keyword"},
                    "rule_name": {"type": "keyword"},
                    "description": {"type": "text"},
                    "severity": {"type": "keyword"},
                    "location_id": {"type": "keyword"},
                    "event_count": {"type": "integer"},
                    "time_window": {"type": "integer"},
                    "status": {"type": "keyword"},
                    "related_events": {"type": "nested"},
                    "risk_score": {"type": "float"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        
        try:
            index_name = f"crpf-alerts-{datetime.now().strftime('%Y.%m.%d')}"
            response = requests.put(
                f"{self.opensearch_url}/{index_name}",
                json=alert_mapping,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [200, 400]:  # 400 if already exists
                logger.info(f"✅ Alert index ready: {index_name}")
            else:
                logger.error(f"❌ Failed to create alert index: {response.text}")
        except Exception as e:
            logger.error(f"❌ Error creating alert index: {e}")

    def evaluate_rules(self, event):
        """Evaluate incoming event against alert rules"""
        location_id = event.get('location_id', 'unknown')
        timestamp = datetime.fromisoformat(event['@timestamp'].replace('Z', '+00:00'))
        
        # Add event to buffer
        self.event_buffers[location_id].append({
            'timestamp': timestamp,
            'event': event
        })
        
        # Check each rule
        for rule_name, rule_config in self.alert_rules.items():
            if self.check_rule_condition(event, rule_config, location_id):
                alert_key = f"{rule_name}_{location_id}"
                
                # Check if alert already exists and is recent
                if alert_key in self.active_alerts:
                    last_alert_time = self.active_alerts[alert_key]['timestamp']
                    if (timestamp - last_alert_time).total_seconds() < rule_config['time_window']:
                        continue  # Skip duplicate alert
                
                # Create new alert
                alert = self.create_alert(rule_name, rule_config, event, location_id)
                if alert:
                    self.send_alert(alert)
                    self.active_alerts[alert_key] = {
                        'timestamp': timestamp,
                        'alert': alert
                    }

    def check_rule_condition(self, event, rule_config, location_id):
        """Check if event matches rule condition"""
        condition = rule_config['condition']
        
        # Simple condition parsing (can be enhanced)
        if 'event_type:' in condition:
            event_type = condition.split('event_type:')[1].split()[0]
            if event.get('event_type') != event_type:
                return False
        
        if 'risk_score>=' in condition:
            min_score = int(condition.split('risk_score>=')[1].split()[0])
            if event.get('risk_score', 0) < min_score:
                return False
        
        if 'threat_level:' in condition:
            threat_level = condition.split('threat_level:')[1].split()[0]
            if event.get('threat_level') != threat_level:
                return False
        
        if 'event_category:' in condition:
            category = condition.split('event_category:')[1].split()[0]
            if event.get('event_category') != category:
                return False
        
        # Check threshold within time window
        current_time = datetime.fromisoformat(event['@timestamp'].replace('Z', '+00:00'))
        time_window = rule_config['time_window']
        threshold = rule_config['threshold']
        
        matching_events = []
        for buffered_event in self.event_buffers[location_id]:
            if (current_time - buffered_event['timestamp']).total_seconds() <= time_window:
                if self.event_matches_condition(buffered_event['event'], condition):
                    matching_events.append(buffered_event['event'])
        
        return len(matching_events) >= threshold

    def event_matches_condition(self, event, condition):
        """Check if a single event matches the condition"""
        if 'event_type:' in condition:
            event_type = condition.split('event_type:')[1].split()[0]
            if event.get('event_type') != event_type:
                return False
        
        if 'risk_score>=' in condition:
            min_score = int(condition.split('risk_score>=')[1].split()[0])
            if event.get('risk_score', 0) < min_score:
                return False
        
        return True

    def create_alert(self, rule_name, rule_config, triggering_event, location_id):
        """Create alert object"""
        alert_id = f"{rule_name}_{location_id}_{int(time.time())}"
        
        # Get related events from buffer
        related_events = []
        current_time = datetime.fromisoformat(triggering_event['@timestamp'].replace('Z', '+00:00'))
        
        for buffered_event in list(self.event_buffers[location_id])[-20:]:  # Last 20 events
            if (current_time - buffered_event['timestamp']).total_seconds() <= rule_config['time_window']:
                if self.event_matches_condition(buffered_event['event'], rule_config['condition']):
                    related_events.append({
                        'event_id': buffered_event['event'].get('event_id'),
                        'event_type': buffered_event['event'].get('event_type'),
                        'timestamp': buffered_event['timestamp'].isoformat(),
                        'user': buffered_event['event'].get('user'),
                        'source_ip': buffered_event['event'].get('source_ip')
                    })
        
        alert = {
            '@timestamp': datetime.now(timezone.utc).isoformat(),
            'alert_id': alert_id,
            'rule_name': rule_name,
            'description': rule_config['description'],
            'severity': rule_config['severity'],
            'location_id': location_id,
            'location_info': triggering_event.get('location_info', {}),
            'event_count': len(related_events),
            'time_window': rule_config['time_window'],
            'threshold': rule_config['threshold'],
            'status': 'ACTIVE',
            'related_events': related_events,
            'triggering_event': {
                'event_id': triggering_event.get('event_id'),
                'event_type': triggering_event.get('event_type'),
                'user': triggering_event.get('user'),
                'source_ip': triggering_event.get('source_ip'),
                'risk_score': triggering_event.get('risk_score')
            },
            'risk_score': max([e.get('risk_score', 0) for e in [triggering_event] + [re['event'] for re in list(self.event_buffers[location_id])[-10:]]], default=0)
        }
        
        return alert

    def send_alert(self, alert):
        """Send alert to OpenSearch and log"""
        try:
            # Index to OpenSearch
            index_name = f"crpf-alerts-{datetime.now().strftime('%Y.%m.%d')}"
            response = requests.post(
                f"{self.opensearch_url}/{index_name}/_doc",
                json=alert,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [200, 201]:
                logger.warning(f"🚨 ALERT: {alert['severity']} - {alert['description']} at {alert['location_id']}")
                logger.info(f"   Alert ID: {alert['alert_id']}")
                logger.info(f"   Event Count: {alert['event_count']}")
                logger.info(f"   Risk Score: {alert['risk_score']}")
            else:
                logger.error(f"❌ Failed to send alert: {response.text}")
                
        except Exception as e:
            logger.error(f"❌ Error sending alert: {e}")

    def cleanup_old_alerts(self):
        """Clean up old active alerts"""
        current_time = datetime.now(timezone.utc)
        expired_alerts = []
        
        for alert_key, alert_data in self.active_alerts.items():
            alert_age = (current_time - alert_data['timestamp']).total_seconds()
            if alert_age > 3600:  # 1 hour
                expired_alerts.append(alert_key)
        
        for key in expired_alerts:
            del self.active_alerts[key]
        
        if expired_alerts:
            logger.info(f"🧹 Cleaned up {len(expired_alerts)} expired alerts")

    def start_monitoring(self):
        """Start alert monitoring"""
        if not self.connect_kafka():
            return False
        
        self.create_alert_index()
        self.running = True
        
        logger.info("🚨 CRPF Alert Manager started")
        
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                event = message.value
                self.evaluate_rules(event)
                
                # Periodic cleanup
                if int(time.time()) % 300 == 0:  # Every 5 minutes
                    self.cleanup_old_alerts()
                    
        except KeyboardInterrupt:
            logger.info("⏹️ Alert monitoring stopped")
        except Exception as e:
            logger.error(f"❌ Alert manager error: {e}")
        finally:
            self.stop_monitoring()

    def stop_monitoring(self):
        """Stop alert monitoring"""
        self.running = False
        if self.consumer:
            self.consumer.close()
        logger.info("✅ Alert manager stopped")

if __name__ == "__main__":
    alert_manager = CRPFAlertManager()
    alert_manager.start_monitoring()
