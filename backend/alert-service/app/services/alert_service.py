import uuid
from datetime import datetime
from typing import List, Set
from fastapi import WebSocket
from app.models.alert import Alert, AlertType, AlertSeverity
from app.database.repositories.alert_repository import AlertRepository
from app.config import settings

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict) -> None:
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

class AlertService:
    def __init__(self, repository: AlertRepository):
        self._repository = repository

    def get_active_alerts(self) -> List[Alert]:
        return self._repository.get_active_alerts()

    def get_all_alerts(self, limit: int = 100) -> List[Alert]:
        return self._repository.get_all_alerts(limit)

    def resolve_alert(self, alert_id: str) -> None:
        self._repository.resolve_alert(alert_id)

    async def check_and_create_alert(self, event: dict) -> None:
        alerts = []

        if event['latency_ms'] > settings.LATENCY_THRESHOLD:
            alerts.append(self._create_alert(
                device_id=event['device_id'],
                location=event['location'],
                alert_type=AlertType.HIGH_LATENCY,
                severity=AlertSeverity.CRITICAL if event['latency_ms'] > 200 else AlertSeverity.WARNING,
                message=f"High latency detected: {event['latency_ms']}ms",
                value=event['latency_ms'],
                threshold=settings.LATENCY_THRESHOLD
            ))

        if event['packet_loss'] > settings.PACKET_LOSS_THRESHOLD:
            alerts.append(self._create_alert(
                device_id=event['device_id'],
                location=event['location'],
                alert_type=AlertType.HIGH_PACKET_LOSS,
                severity=AlertSeverity.CRITICAL if event['packet_loss'] > 10 else AlertSeverity.WARNING,
                message=f"High packet loss detected: {event['packet_loss']}%",
                value=event['packet_loss'],
                threshold=settings.PACKET_LOSS_THRESHOLD
            ))

        if event['signal_strength_dbm'] < settings.SIGNAL_THRESHOLD:
            alerts.append(self._create_alert(
                device_id=event['device_id'],
                location=event['location'],
                alert_type=AlertType.LOW_SIGNAL,
                severity=AlertSeverity.WARNING,
                message=f"Low signal strength: {event['signal_strength_dbm']}dBm",
                value=event['signal_strength_dbm'],
                threshold=settings.SIGNAL_THRESHOLD
            ))

        for alert in alerts:
            self._repository.insert(alert)
            await manager.broadcast(alert.model_dump(mode='json'))

    def _create_alert(
        self,
        device_id: str,
        location: str,
        alert_type: AlertType,
        severity: AlertSeverity,
        message: str,
        value: float,
        threshold: float
    ) -> Alert:
        return Alert(
            alert_id=str(uuid.uuid4()),
            device_id=device_id,
            location=location,
            alert_type=alert_type,
            severity=severity,
            message=message,
            value=value,
            threshold=threshold,
            timestamp=datetime.utcnow(),
            resolved=False
        )

alert_service = AlertService(repository=AlertRepository())