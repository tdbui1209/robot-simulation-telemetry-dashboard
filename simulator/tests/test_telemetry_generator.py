from datetime import datetime

from simulator.robot_simulator.generator import TelemetryGenerator


def test_next_packet_returns_dict(experiment_config):
    generator = TelemetryGenerator(experiment_config)

    packet = generator.next_packet()

    assert isinstance(packet, dict)


def test_next_packet_contains_required_metadata_fields(experiment_config):
    generator = TelemetryGenerator(experiment_config)

    packet = generator.next_packet()

    assert packet["schema_version"] == "1.0"
    assert packet["experiment_id"] == "exp_test_001"
    assert packet["run_id"] == "run_test_001"
    assert packet["robot_id"] == "humanoid_sim_01"
    assert "timestamp" in packet
    assert "sequence" in packet
    assert "sim_time" in packet
    assert "base_pose" in packet
    assert "sensors" in packet
    assert "control_command" in packet
    assert "metrics" in packet
    assert "events" in packet
    assert "position" in packet["base_pose"]
    assert "orientation" in packet["base_pose"]
    assert "linear_velocity" in packet["base_pose"]
    assert "angular_velocity" in packet["base_pose"]
    assert "mode" in packet["control_command"]
    assert "target_velocity" in packet["control_command"]
    assert "x" in packet["base_pose"]["position"]
    assert "y" in packet["base_pose"]["position"]
    assert "z" in packet["base_pose"]["position"]
    assert "roll" in packet["base_pose"]["orientation"]
    assert "pitch" in packet["base_pose"]["orientation"]
    assert "yaw" in packet["base_pose"]["orientation"]
    assert "vx" in packet["base_pose"]["linear_velocity"]
    assert "vy" in packet["base_pose"]["linear_velocity"]
    assert "vz" in packet["base_pose"]["linear_velocity"]
    assert "wx" in packet["base_pose"]["angular_velocity"]
    assert "wy" in packet["base_pose"]["angular_velocity"]
    assert "wz" in packet["base_pose"]["angular_velocity"]


def test_timestamp_is_iso_format_and_timezone_aware(experiment_config):
    generator = TelemetryGenerator(experiment_config)

    packet = generator.next_packet()
    parsed_timestamp = datetime.fromisoformat(packet["timestamp"])

    assert parsed_timestamp.tzinfo is not None


def test_sim_time_increases_by_dt(experiment_config):
    generator = TelemetryGenerator(experiment_config)

    first_packet = generator.next_packet()
    second_packet = generator.next_packet()

    expected_dt = 1.0 / experiment_config["experiment"]["frequency_hz"]

    assert first_packet["sim_time"] == expected_dt
    assert second_packet["sim_time"] == expected_dt * 2
