import random


def generate_metrics(hz:float, sim_step_ms: float, latency_std_ms: float) -> dict:
    latency = max(1.0, random.gauss(18.0, latency_std_ms))
    return {
        "fps": hz,
        "sim_step_ms": sim_step_ms,
        "latency_ms": latency,
        "packet_size_bytes": 1800,
    }
