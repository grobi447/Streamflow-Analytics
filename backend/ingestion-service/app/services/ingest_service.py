import uuid
from datetime import datetime
from app.models.network_event import NetworkEvent
from app.models.responses import IngestResponse
from app.database.repositories.event_repository import EventRepository
from app.kafka.producer import kafka_producer
from app.config import settings

class IngestService:
    def __init__(self, repository: EventRepository):
        self._repository = repository

    def process(self, event: NetworkEvent) -> IngestResponse:
        event_id = str(uuid.uuid4())
        event_dict = event.model_dump()
        event_dict['event_id'] = event_id

        kafka_producer.send(settings.kafka_topic, event_dict)
        self._repository.insert(event_id, event)

        return IngestResponse(
            status="success",
            event_id=event_id,
            device_id=event.device_id,
            timestamp=event.timestamp,
            message=f"Event from {event.device_id} processed"
        )

ingest_service = IngestService(repository=EventRepository())