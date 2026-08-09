import pytest


@pytest.fixture
def valid_telemetry_packet() -> dict:
    return {
        "schema_version": "1.0",
        "timestamp": "2026-08-09T02:30:00+00:00",
        "experiment_id": "exp_walk_001",
        "run_id": "run_local_001",
        "robot_id": "humanoid_sim_01",
        "sequence": 1,
        "sim_time": 0.033,
        "base_pose": {
            "position": {
                "x": 0.01,
                "y": 0.0,
                "z": 0.94,
            },
            "orientation": {
                "roll": 0.01,
                "pitch": 0.02,
                "yaw": 0.03,
            },
            "linear_velocity": {
                "vx": 0.5,
                "vy": 0.0,
                "vz": 0.0,
            },
            "angular_velocity": {
                "wx": 0.01,
                "wy": 0.02,
                "wz": 0.05,
            },
        },
        "sensors": {
            "imu": {
                "acceleration": {
                    "ax": 0.1,
                    "ay": 0.0,
                    "az": 9.81,
                },
                "gyroscope": {
                    "gx": 0.01,
                    "gy": 0.02,
                    "gz": 0.03,
                },
            },
            "foot_contact": {
                "left": 1.0,
                "right": 1.0,
                "left_force": 290.0,
                "right_force": 295.0,
            },
        },
        "metrics": {
            "fps": 30.0,
            "sim_step_ms": 4.2,
            "latency_ms": 5.1,
            "packet_size_bytes": 1024,
            "stability_score": 0.98,
            "tracking_error": 0.01,
        },
        "events": [
            {
                "type": "info",
                "severity": "low",
                "message": "simulation running",
                "value": None,
            }
        ],
    }
