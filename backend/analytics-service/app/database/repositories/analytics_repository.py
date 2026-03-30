from typing import List
from app.database.connection import vertica_connection
from app.models.analytics import (
    DeviceSummary,
    LocationSummary,
    TrendPoint,
    TopLatencyDevice,
    NetworkSummary
)

class AnalyticsRepository:
    def get_network_summary(self) -> NetworkSummary:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    COUNT(*) as total_events,
                    COUNT(DISTINCT device_id) as total_devices,
                    COUNT(DISTINCT location) as total_locations,
                    AVG(latency_ms) as avg_latency_ms,
                    AVG(packet_loss) as avg_packet_loss,
                    AVG(bandwidth_mbps) as avg_bandwidth_mbps
                FROM network_events
            """)
            row = cursor.fetchone()
            return NetworkSummary(
                total_events=row[0],
                total_devices=row[1],
                total_locations=row[2],
                avg_latency_ms=round(row[3] or 0, 2),
                avg_packet_loss=round(row[4] or 0, 2),
                avg_bandwidth_mbps=round(row[5] or 0, 2)
            )

    def get_device_summary(self, device_id: str) -> DeviceSummary:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""...""", (device_id,))
            row = cursor.fetchone()
            if row is None:
                raise ValueError(f"Device {device_id} not found")
            return DeviceSummary(...)
    
    def get_location_summary(self, location: str) -> LocationSummary:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    location,
                    AVG(latency_ms) as avg_latency_ms,
                    AVG(packet_loss) as avg_packet_loss,
                    AVG(bandwidth_mbps) as avg_bandwidth_mbps,
                    COUNT(DISTINCT device_id) as total_devices,
                    COUNT(*) as total_events
                FROM network_events
                WHERE location = %s
                GROUP BY location
            """, (location,))
            row = cursor.fetchone()
            return LocationSummary(
                location=row[0],
                avg_latency_ms=round(row[1], 2),
                avg_packet_loss=round(row[2], 2),
                avg_bandwidth_mbps=round(row[3], 2),
                total_devices=row[4],
                total_events=row[5]
            )

    def get_top_latency_devices(self, limit: int = 10) -> List[TopLatencyDevice]:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    device_id,
                    location,
                    AVG(latency_ms) as avg_latency_ms
                FROM network_events
                GROUP BY device_id, location
                ORDER BY avg_latency_ms DESC
                LIMIT %s
            """, (limit,))
            rows = cursor.fetchall()
            return [
                TopLatencyDevice(
                    device_id=row[0],
                    location=row[1],
                    avg_latency_ms=round(row[2], 2)
                )
                for row in rows
            ]

    def get_trends(self, hours: int = 24) -> List[TrendPoint]:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    DATE_TRUNC('hour', timestamp) as hour,
                    AVG(latency_ms) as avg_latency_ms,
                    AVG(packet_loss) as avg_packet_loss,
                    AVG(bandwidth_mbps) as avg_bandwidth_mbps,
                    COUNT(*) as total_events
                FROM network_events
                WHERE timestamp >= NOW() - INTERVAL '%s hours'
                GROUP BY DATE_TRUNC('hour', timestamp)
                ORDER BY hour ASC
            """, (hours,))
            rows = cursor.fetchall()
            return [
                TrendPoint(
                    timestamp=row[0],
                    avg_latency_ms=round(row[1], 2),
                    avg_packet_loss=round(row[2], 2),
                    avg_bandwidth_mbps=round(row[3], 2),
                    total_events=row[4]
                )
                for row in rows
            ]
        
    def get_all_devices(self) -> List[DeviceSummary]:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    device_id,
                    location,
                    AVG(latency_ms) as avg_latency_ms,
                    AVG(packet_loss) as avg_packet_loss,
                    AVG(bandwidth_mbps) as avg_bandwidth_mbps,
                    AVG(signal_strength_dbm) as avg_signal_strength_dbm,
                    COUNT(*) as total_events
                FROM network_events
                GROUP BY device_id, location
                ORDER BY avg_latency_ms DESC
            """)
            rows = cursor.fetchall()
            return [
                DeviceSummary(
                    device_id=row[0],
                    location=row[1],
                    avg_latency_ms=round(row[2], 2),
                    avg_packet_loss=round(row[3], 2),
                    avg_bandwidth_mbps=round(row[4], 2),
                    avg_signal_strength_dbm=round(row[5], 2),
                    total_events=row[6]
                )
                for row in rows
            ]
        
    def get_trends_minutes(self, minutes: int = 60) -> List[TrendPoint]:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    DATE_TRUNC('minute', timestamp) as minute,
                    AVG(latency_ms) as avg_latency_ms,
                    AVG(packet_loss) as avg_packet_loss,
                    AVG(bandwidth_mbps) as avg_bandwidth_mbps,
                    COUNT(*) as total_events
                FROM network_events
                WHERE timestamp >= NOW() - INTERVAL '%s minutes'
                GROUP BY DATE_TRUNC('minute', timestamp)
                ORDER BY minute ASC
            """, (minutes,))
            rows = cursor.fetchall()
            return [
                TrendPoint(
                    timestamp=row[0],
                    avg_latency_ms=round(row[1], 2),
                    avg_packet_loss=round(row[2], 2),
                    avg_bandwidth_mbps=round(row[3], 2),
                    total_events=row[4]
                )
                for row in rows
            ]
        
    def get_latest_device_values(self) -> List[DeviceSummary]:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    e.device_id,
                    e.location,
                    e.latency_ms as avg_latency_ms,
                    e.packet_loss as avg_packet_loss,
                    e.bandwidth_mbps as avg_bandwidth_mbps,
                    e.signal_strength_dbm as avg_signal_strength_dbm,
                    1 as total_events
                FROM network_events e
                INNER JOIN (
                    SELECT device_id, MAX(timestamp) as max_ts
                    FROM network_events
                    GROUP BY device_id
                ) latest ON e.device_id = latest.device_id AND e.timestamp = latest.max_ts
            """)
            rows = cursor.fetchall()
            return [
                DeviceSummary(
                    device_id=row[0],
                    location=row[1],
                    avg_latency_ms=round(row[2], 2),
                    avg_packet_loss=round(row[3], 2),
                    avg_bandwidth_mbps=round(row[4], 2),
                    avg_signal_strength_dbm=round(row[5], 2),
                    total_events=row[6]
                )
                for row in rows
            ]