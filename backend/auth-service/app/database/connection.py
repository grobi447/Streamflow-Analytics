import vertica_python
from app.config import settings

class VerticaConnection:
    def __init__(self):
        self._conn_info = {
            'host': settings.VERTICA_HOST,
            'port': settings.VERTICA_PORT,
            'user': settings.VERTICA_USER,
            'password': settings.VERTICA_PASSWORD,
            'database': settings.VERTICA_DATABASE,
        }

    def get_connection(self) -> vertica_python.Connection:
        return vertica_python.connect(**self._conn_info)

vertica_connection = VerticaConnection()