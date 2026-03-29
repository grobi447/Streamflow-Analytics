import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "network.events")
INGESTION_SERVICE_URL = os.getenv("INGESTION_SERVICE_URL", "http://localhost:8002")
EVENTS_PER_SECOND = int(os.getenv("EVENTS_PER_SECOND", "10"))
NUM_TOWERS = int(os.getenv("NUM_TOWERS", "100"))

LOCATIONS = [
    "Budapest", "Debrecen", "Pécs", "Győr",
    "Miskolc", "Szeged", "Székesfehérvár",
    "Kecskemét", "Nyíregyháza", "Eger"
]

TOWERS = [
    {
        "device_id": f"tower_{i:03d}",
        "location": LOCATIONS[i % len(LOCATIONS)]
    }
    for i in range(NUM_TOWERS)
]