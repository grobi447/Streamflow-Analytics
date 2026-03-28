from typing import Protocol
from app.models.network_event import NetworkEvent
from app.database.connection import vertica_connection

class IEventRepository(Protocol):
    def insert(self, event_id: str, event: NetworkEvent) -> None: ...
    def init_table(self) -> None: ...

class EventRepository:
    def init_table(self) -> None:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS network_events (
                    event_id            VARCHAR(36),
                    device_id           VARCHAR(50),
                    location            VARCHAR(100),
                    timestamp           TIMESTAMP,
                    latency_ms          FLOAT,
                    packet_loss         FLOAT,
                    bandwidth_mbps      FLOAT,
                    active_connections  INTEGER,
                    signal_strength_dbm FLOAT
                )
            """)
            conn.commit()

    def insert(self, event_id: str, event: NetworkEvent) -> None:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO network_events (
                    event_id, device_id, location, timestamp,
                    latency_ms, packet_loss, bandwidth_mbps,
                    active_connections, signal_strength_dbm
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                event_id,
                event.device_id,
                event.location.value,
                event.timestamp,
                event.latency_ms,
                event.packet_loss,
                event.bandwidth_mbps,
                event.active_connections,
                event.signal_strength_dbm
            ))
            conn.commit()