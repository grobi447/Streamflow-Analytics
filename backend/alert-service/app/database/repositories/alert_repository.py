import uuid
from datetime import datetime
from typing import List
from app.database.connection import vertica_connection
from app.models.alert import Alert, AlertType, AlertSeverity

class AlertRepository:
    def init_table(self) -> None:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    alert_id    VARCHAR(36),
                    device_id   VARCHAR(50),
                    location    VARCHAR(100),
                    alert_type  VARCHAR(50),
                    severity    VARCHAR(20),
                    message     VARCHAR(500),
                    value       FLOAT,
                    threshold   FLOAT,
                    timestamp   TIMESTAMP,
                    resolved    BOOLEAN DEFAULT FALSE
                )
            """)
            conn.commit()

    def insert(self, alert: Alert) -> None:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO alerts (
                    alert_id, device_id, location, alert_type,
                    severity, message, value, threshold, timestamp, resolved
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                alert.alert_id,
                alert.device_id,
                alert.location,
                alert.alert_type.value,
                alert.severity.value,
                alert.message,
                alert.value,
                alert.threshold,
                alert.timestamp,
                alert.resolved
            ))
            conn.commit()

    def get_active_alerts(self) -> List[Alert]:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    alert_id, device_id, location, alert_type,
                    severity, message, value, threshold, timestamp, resolved
                FROM alerts
                WHERE resolved = FALSE
                ORDER BY timestamp DESC
            """)
            rows = cursor.fetchall()
            return [self._row_to_alert(row) for row in rows]

    def get_all_alerts(self, limit: int = 100) -> List[Alert]:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    alert_id, device_id, location, alert_type,
                    severity, message, value, threshold, timestamp, resolved
                FROM alerts
                ORDER BY timestamp DESC
                LIMIT %s
            """, (limit,))
            rows = cursor.fetchall()
            return [self._row_to_alert(row) for row in rows]

    def resolve_alert(self, alert_id: str) -> None:
        with vertica_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE alerts SET resolved = TRUE
                WHERE alert_id = %s
            """, (alert_id,))
            conn.commit()

    def _row_to_alert(self, row) -> Alert:
        return Alert(
            alert_id=row[0],
            device_id=row[1],
            location=row[2],
            alert_type=AlertType(row[3]),
            severity=AlertSeverity(row[4]),
            message=row[5],
            value=row[6],
            threshold=row[7],
            timestamp=row[8],
            resolved=row[9]
        )