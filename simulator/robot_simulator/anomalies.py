import random


def anomaly_flags(config: dict) -> dict:
    anomalies = config["anomalies"]
    if not anomalies["enabled"]:
        return {}
    return {
        "latency_spike": random.random() < anomalies.get("latency_spike_probability", 0),
        "packet_drop": random.random() < anomalies.get("packet_drop_probability", 0),
    }
