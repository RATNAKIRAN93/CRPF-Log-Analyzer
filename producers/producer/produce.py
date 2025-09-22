import os, time, json, random, socket
from kafka import KafkaProducer
from datetime import datetime

broker = os.getenv("KAFKA_BROKER", "kafka:9092")
endpoint = os.getenv("ENDPOINT_NAME", socket.gethostname())
topic = "system-logs"

producer = KafkaProducer(bootstrap_servers=[broker],
                         value_serializer=lambda v: json.dumps(v).encode("utf-8"))

levels = ["INFO", "WARN", "ERROR", "DEBUG"]
users = ["alice","bob","system","admin"]

def gen_event():
    now = datetime.utcnow().isoformat() + "Z"
    ev = {
        "timestamp": now,
        "endpoint": endpoint,
        "level": random.choices(levels, weights=[0.6,0.2,0.15,0.05])[0],
        "message": random.choice([
            "User logged in",
            "Failed password attempt",
            "File deleted",
            "Process started",
            "Unusual network connection",
            "Service crashed",
            "Configuration changed"
        ]),
        "user": random.choice(users),
        "src_ip": f"10.0.{random.randint(0,5)}.{random.randint(1,254)}",
        "dest_ip": f"192.168.{random.randint(0,5)}.{random.randint(1,254)}",
        "pid": random.randint(100,5000)
    }
    return ev

if __name__ == "__main__":
    while True:
        ev = gen_event()
        producer.send(topic, ev)
        print("sent", ev)
        # variable sleep to simulate bursty logs
        time.sleep(random.uniform(0.2, 2.0))
