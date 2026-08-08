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
            },
            "gait_frequency_hz": 1.2,
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
