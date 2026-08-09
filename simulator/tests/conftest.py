from pathlib import Path

import pytest
import yaml


@pytest.fixture
def experiment_config() -> dict:
    return {
        "experiment": {
            "id": "exp_test_001",
            "run_id": "run_test_001",
            "robot_id": "humanoid_sim_01",
            "duration_sec": 10,
            "frequency_hz": 30,
            "random_state": 42,
        },
        "robot": {
            "mass_kg": 60,
            "base_height_m": 0.94,
        },
        "motion": {
            "mode": "walk",
            "target_velocity": {
                "vx": 0.5,
                "vy": 0.0,
                "yaw_rate": 0.05,
            },
            "gait_frequency_hz": 1.2,
            "lateral_sway_m": 0.03,
            "vertical_bob_m": 0.025,
            "roll_factor_std": 0.07,
            "pitch_factor_std": 0.08,
        },
        "noise": {
            "imu_accel_std": 0.03,
            "gyro_std": 0.005,
            "latency_std_ms": 5,
            "foot_force_std_n": 15,
        },
        "anomalies": {
            "enabled": True,
            "latency_spike_probability": 0.01,
            "packet_drop_probability": 0.005,
        }
    }


@pytest.fixture
def experiment_config_file(tmp_path: Path, experiment_config: dict) -> Path:
    config_path = tmp_path / "experiment_test.yaml"
    config_path.write_text(
        yaml.safe_dump(experiment_config),
        encoding="utf-8",
    )
    return config_path
