import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "network.events")
EVENTS_PER_SECOND = int(os.getenv("EVENTS_PER_SECOND", "10"))
NUM_TOWERS = int(os.getenv("NUM_TOWERS", "100"))

# ANOMALY_CONFIG
ANOMALY_PROBABILITY = float(os.getenv("ANOMALY_PROBABILITY", "0.3"))  # 30%
ANOMALY_DURATION_SECONDS = int(os.getenv("ANOMALY_DURATION_SECONDS", "30"))  # 30sec
HIGH_LATENCY_MIN = float(os.getenv("HIGH_LATENCY_MIN", "100"))
HIGH_LATENCY_MAX = float(os.getenv("HIGH_LATENCY_MAX", "800"))
HIGH_PACKET_LOSS_MIN = float(os.getenv("HIGH_PACKET_LOSS_MIN", "5"))
HIGH_PACKET_LOSS_MAX = float(os.getenv("HIGH_PACKET_LOSS_MAX", "25"))
LOW_SIGNAL_MIN = float(os.getenv("LOW_SIGNAL_MIN", "-100"))
LOW_SIGNAL_MAX = float(os.getenv("LOW_SIGNAL_MAX", "-90"))
LOW_BANDWIDTH_MIN = float(os.getenv("LOW_BANDWIDTH_MIN", "10"))
LOW_BANDWIDTH_MAX = float(os.getenv("LOW_BANDWIDTH_MAX", "80"))

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