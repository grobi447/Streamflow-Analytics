import json
import time
import random
import uuid
import logging
from datetime import datetime
from kafka import KafkaProducer
from config import (
    KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, TOWERS, EVENTS_PER_SECOND,
    ANOMALY_PROBABILITY, ANOMALY_DURATION_SECONDS,
    HIGH_LATENCY_MIN, HIGH_LATENCY_MAX,
    HIGH_PACKET_LOSS_MIN, HIGH_PACKET_LOSS_MAX,
    LOW_SIGNAL_MIN, LOW_SIGNAL_MAX,
    LOW_BANDWIDTH_MIN, LOW_BANDWIDTH_MAX
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Anomália state per tower
tower_anomaly_state: dict = {}

def get_tower_state(tower_id: str) -> dict:
    if tower_id not in tower_anomaly_state:
        tower_anomaly_state[tower_id] = {
            'in_anomaly': False,
            'anomaly_type': None,
            'anomaly_until': 0
        }
    return tower_anomaly_state[tower_id]

def generate_event(tower: dict) -> dict:
    state = get_tower_state(tower['device_id'])
    now = time.time()

    if state['in_anomaly'] and now > state['anomaly_until']:
        state['in_anomaly'] = False
        state['anomaly_type'] = None

    if not state['in_anomaly'] and random.random() < ANOMALY_PROBABILITY:
        state['in_anomaly'] = True
        state['anomaly_type'] = random.choice(['latency', 'packet_loss', 'signal', 'bandwidth'])
        state['anomaly_until'] = now + ANOMALY_DURATION_SECONDS

    event = {
        "event_id": str(uuid.uuid4()),
        "device_id": tower["device_id"],
        "location": tower["location"],
        "timestamp": datetime.now().isoformat(),
        "latency_ms": round(random.uniform(10, 50), 2),
        "packet_loss": round(random.uniform(0, 1.5), 2),
        "bandwidth_mbps": round(random.uniform(300, 1000), 2),
        "active_connections": random.randint(500, 2000),
        "signal_strength_dbm": round(random.uniform(-80, -50), 2)
    }

    if state['in_anomaly']:
        t = state['anomaly_type']
        if t == 'latency':
            event['latency_ms'] = round(random.uniform(HIGH_LATENCY_MIN, HIGH_LATENCY_MAX), 2)
            event['active_connections'] = random.randint(1500, 3000)
        elif t == 'packet_loss':
            event['packet_loss'] = round(random.uniform(HIGH_PACKET_LOSS_MIN, HIGH_PACKET_LOSS_MAX), 2)
            event['latency_ms'] = round(random.uniform(60, 150), 2)
        elif t == 'signal':
            event['signal_strength_dbm'] = round(random.uniform(LOW_SIGNAL_MIN, LOW_SIGNAL_MAX), 2)
            event['latency_ms'] = round(random.uniform(80, 200), 2)
        elif t == 'bandwidth':
            event['bandwidth_mbps'] = round(random.uniform(LOW_BANDWIDTH_MIN, LOW_BANDWIDTH_MAX), 2)
            event['latency_ms'] = round(random.uniform(70, 180), 2)

    return event

def main():
    logger.info(f"Starting simulator...")
    logger.info(f"Kafka: {KAFKA_BOOTSTRAP_SERVERS}")
    logger.info(f"Topic: {KAFKA_TOPIC}")
    logger.info(f"Towers: {len(TOWERS)}")
    logger.info(f"Events/sec: {EVENTS_PER_SECOND}")
    logger.info(f"Anomaly probability: {ANOMALY_PROBABILITY * 100}%")
    logger.info(f"Anomaly duration: {ANOMALY_DURATION_SECONDS}s")

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
    )

    event_count = 0
    start_time = time.time()

    while True:
        tower = random.choice(TOWERS)
        event = generate_event(tower)
        producer.send(KAFKA_TOPIC, event)
        producer.flush()

        event_count += 1
        elapsed = time.time() - start_time

        if event_count % 100 == 0:
            anomaly_count = sum(1 for s in tower_anomaly_state.values() if s['in_anomaly'])
            logger.info(f"Sent {event_count} events | {event_count/elapsed:.1f} eps | {anomaly_count} towers in anomaly")

        time.sleep(1 / EVENTS_PER_SECOND)

if __name__ == "__main__":
    main()
