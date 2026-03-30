from typing import List
from app.models.analytics import (
    DeviceSummary,
    LocationSummary,
    TrendPoint,
    TopLatencyDevice,
    NetworkSummary
)
from app.database.repositories.analytics_repository import AnalyticsRepository

class AnalyticsService:
    def __init__(self, repository: AnalyticsRepository):
        self._repository = repository

    def get_summary(self) -> NetworkSummary:
        return self._repository.get_network_summary()

    def get_device(self, device_id: str) -> DeviceSummary:
        return self._repository.get_device_summary(device_id)

    def get_location(self, location: str) -> LocationSummary:
        return self._repository.get_location_summary(location)

    def get_top_latency(self, limit: int = 10) -> List[TopLatencyDevice]:
        return self._repository.get_top_latency_devices(limit)

    def get_trends(self, hours: int = 24) -> List[TrendPoint]:
        return self._repository.get_trends(hours)

    def get_all_devices(self) -> List[DeviceSummary]:
        return self._repository.get_all_devices()

    def get_trends_minutes(self, minutes: int) -> List[TrendPoint]:
        return self._repository.get_trends_minutes(minutes)

    def get_latest_device_values(self) -> List[DeviceSummary]:
        return self._repository.get_latest_device_values()

analytics_service = AnalyticsService(repository=AnalyticsRepository())