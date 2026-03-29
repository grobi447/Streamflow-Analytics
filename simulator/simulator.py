import json
import time
import random
import uuid
from datetime import datetime
from kafka import KafkaProducer
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, TOWERS, EVENTS_PER_SECOND
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_normal_event(tower: dict) -> dict:
    return {
        "event_id": str(uuid.uuid4()),
        "device_id": tower["device_id"],
        "location": tower["location"],
        "timestamp": datetime.utcnow().isoformat(),
        "latency_ms": round(random.uniform(10, 50), 2),
        "packet_loss": round(random.uniform(0, 1), 2),
        "bandwidth_mbps": round(random.uniform(200, 1000), 2),
        "active_connections": random.randint(500, 2000),
        "signal_strength_dbm": round(random.uniform(-80, -50), 2)
    }

def generate_anomaly_event(tower: dict) -> dict:
    anomaly_type = random.choice(["latency", "packet_loss", "signal"])
    event = generate_normal_event(tower)
    if anomaly_type == "latency":
        event["latency_ms"] = round(random.uniform(100, 500), 2)
    elif anomaly_type == "packet_loss":
        event["packet_loss"] = round(random.uniform(5, 20), 2)
    elif anomaly_type == "signal":
        event["signal_strength_dbm"] = round(random.uniform(-100, -90), 2)
    return event

def should_generate_anomaly() -> bool:
    return random.random() < 0.05

def main():
    logger.info(f"Starting simulator...")
    logger.info(f"Kafka: {KAFKA_BOOTSTRAP_SERVERS}")
    logger.info(f"Topic: {KAFKA_TOPIC}")
    logger.info(f"Towers: {len(TOWERS)}")
    logger.info(f"Events/sec: {EVENTS_PER_SECOND}")

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
    )

    event_count = 0
    start_time = time.time()

    while True:
        tower = random.choice(TOWERS)
        event = generate_anomaly_event(tower) if should_generate_anomaly() else generate_normal_event(tower)
        producer.send(KAFKA_TOPIC, event)
        producer.flush()
        event_count += 1
        elapsed = time.time() - start_time
        if event_count % 50 == 0:
            logger.info(f"Sent {event_count} events in {elapsed:.1f}s ({event_count/elapsed:.1f} events/sec)")
        time.sleep(1 / EVENTS_PER_SECOND)

if __name__ == "__main__":
    main()