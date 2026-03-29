import json
import threading
import logging
import time
from kafka import KafkaConsumer
from app.config import settings
from app.models.network_event import NetworkEvent
from app.database.repositories.event_repository import EventRepository
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaEventConsumer:
    def __init__(self, repository: EventRepository):
        self._repository = repository

    def start(self):
        thread = threading.Thread(target=self._consume, daemon=True)
        thread.start()
        logger.info("Kafka consumer thread started")

    def _consume(self):
        logger.info("Connecting to Kafka...")
        time.sleep(2)
        consumer = KafkaConsumer(
            settings.KAFKA_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            group_id="ingestion-service",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            consumer_timeout_ms=-1
        )
        logger.info("Kafka consumer connected, listening for messages...")
        for message in consumer:
            try:
                data = message.value
                logger.info(f"Received event from {data.get('device_id')}")
                event = NetworkEvent(
                    device_id=data['device_id'],
                    location=data['location'],
                    timestamp=data['timestamp'],
                    latency_ms=data['latency_ms'],
                    packet_loss=data['packet_loss'],
                    bandwidth_mbps=data['bandwidth_mbps'],
                    active_connections=data['active_connections'],
                    signal_strength_dbm=data['signal_strength_dbm']
                )
                event_id = data.get('event_id', str(uuid.uuid4()))
                self._repository.insert(event_id, event)
                logger.info(f"Saved event {event_id} to Vertica")
            except Exception as e:
                logger.error(f"Error: {e}")