import vertica_python
from app.config import settings

class VerticaConnection:
    def __init__(self):
        self._conn_info = {
            'host': settings.vertica_host,
            'port': settings.vertica_port,
            'user': settings.vertica_user,
            'password': settings.vertica_password,
            'database': settings.vertica_database,
        }

    def get_connection(self) -> vertica_python.Connection:
        return vertica_python.connect(**self._conn_info)

vertica_connection = VerticaConnection()