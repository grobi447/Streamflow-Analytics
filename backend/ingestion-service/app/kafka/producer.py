import json
from kafka import KafkaProducer as _KafkaProducer
from app.config import settings

class KafkaProducer:
    def __init__(self):
        self._producer = _KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
        )

    def send(self, topic: str, message: dict) -> None:
        self._producer.send(topic, message)
        self._producer.flush()

kafka_producer = KafkaProducer()