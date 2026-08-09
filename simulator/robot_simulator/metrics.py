import random


def generate_metrics(
    hz: float,
    sim_step_ms: float,
    latency_std_ms: float,
    roll: float,
    pitch: float,
    tracking_error: float,
    latency_spike=False,
) -> dict:
    latency = max(1.0, random.gauss(18.0, latency_std_ms))
    if latency_spike:
        latency_spike += random.uniform(50, 120)
    stability = 1.0 - abs(roll) * 2.0 - abs(pitch) * 2.0 - tracking_error * 0.5
    stability = max(0,0, min(1,0, stability))
    return {
        "fps": hz,
        "sim_step_ms": sim_step_ms,
        "latency_ms": latency,
        "packet_size_bytes": 1800,
        "stability_score": stability,
        "tracking_error": tracking_error
    }
