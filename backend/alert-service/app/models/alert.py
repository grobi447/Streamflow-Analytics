from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class AlertType(str, Enum):
    HIGH_LATENCY = "HIGH_LATENCY"
    HIGH_PACKET_LOSS = "HIGH_PACKET_LOSS"
    LOW_SIGNAL = "LOW_SIGNAL"

class AlertSeverity(str, Enum):
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class Alert(BaseModel):
    alert_id: str
    device_id: str
    location: str
    alert_type: AlertType
    severity: AlertSeverity
    message: str
    value: float
    threshold: float
    timestamp: datetime
    resolved: bool = False

class AlertResponse(BaseModel):
    status: str
    message: str

class AlertListResponse(BaseModel):
    total: int
    alerts: list[Alert]