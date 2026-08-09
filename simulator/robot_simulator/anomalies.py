import random


def anomaly_flags(config: dict) -> dict:
    anomalies = config["anomalies"]
    if not anomalies["enabled"]:
        return {}
    return {
        "latency_spike": random.random() < anomalies.get("latency_spike_probability", 0),
        "packet_drop": random.random() < anomalies.get("packet_drop_probability", 0),
    }


def build_event(flags: dict, metrics=None) -> list[dict]:
    events = []
    if flags.get("latency_spike"):
        events.append({
            "type": "latency_spike",
            "severity": "warning",
            "message": "Telemetry latency exceeded threshold",
        })
    if metrics and metrics.get("stability_score", 1) < 0.65:
        events.append({
            "type": "stability_low",
            "severity": "critical",
            "message": "Stability score dropped below threshold",
            "value": metrics["stability_score"]
        })
    return events
