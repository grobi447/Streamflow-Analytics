from pydantic import BaseModel
from datetime import datetime

class DeviceSummary(BaseModel):
    device_id: str
    location: str
    avg_latency_ms: float
    avg_packet_loss: float
    avg_bandwidth_mbps: float
    avg_signal_strength_dbm: float
    total_events: int

class LocationSummary(BaseModel):
    location: str
    avg_latency_ms: float
    avg_packet_loss: float
    avg_bandwidth_mbps: float
    total_devices: int
    total_events: int

class TrendPoint(BaseModel):
    timestamp: datetime
    avg_latency_ms: float
    avg_packet_loss: float
    avg_bandwidth_mbps: float
    total_events: int

class TopLatencyDevice(BaseModel):
    device_id: str
    location: str
    avg_latency_ms: float

class NetworkSummary(BaseModel):
    total_events: int
    total_devices: int
    total_locations: int
    avg_latency_ms: float
    avg_packet_loss: float
    avg_bandwidth_mbps: float