def generate_metrics(hz, sim_step_ms):
    return {
        "fps": hz,
        "sim_step_ms": sim_step_ms,
        "packet_size_bytes": 1800
    }
