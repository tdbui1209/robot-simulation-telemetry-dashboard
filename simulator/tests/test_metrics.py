from simulator.robot_simulator.metrics import generate_metrics


def test_generate_sensors_returns_expected_schema():
    metrics = generate_metrics(1, 1)

    assert "fps" in metrics
    assert "sim_step_ms" in metrics
    assert "packet_size_bytes" in metrics
