from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class Location(str, Enum):
    BUDAPEST = "Budapest"
    DEBRECEN = "Debrecen"
    PECS = "Pécs"
    GYOR = "Győr"
    MISKOLC = "Miskolc"
    SZEGED = "Szeged"
    SZEKESFEHERVAR = "Székesfehérvár"
    KECSKEMET = "Kecskemét"
    NYIREGYHAZA = "Nyíregyháza"
    EGER = "Eger"

class NetworkEvent(BaseModel):
    device_id: str = Field(..., pattern="^tower_[0-9]{3}$")
    location: Location
    timestamp: datetime
    latency_ms: float = Field(..., ge=0)
    packet_loss: float = Field(..., ge=0, le=100)
    bandwidth_mbps: float = Field(..., ge=0)
    active_connections: int = Field(..., ge=0)
    signal_strength_dbm: float = Field(..., le=0)