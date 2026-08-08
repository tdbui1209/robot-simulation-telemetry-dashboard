from simulator.run_simulator import load_config


def test_load_config_returns_dict(experiment_config_file):
    config = load_config(experiment_config_file)

    assert isinstance(config, dict)


def test_load_config_reads_experiment_fields(experiment_config_file):
    config = load_config(experiment_config_file)

    assert config["experiment"]["id"] == "exp_test_001"
    assert config["experiment"]["run_id"] == "run_test_001"
    assert config["experiment"]["robot_id"] == "humanoid_sim_01"
    assert config["experiment"]["duration_sec"] == 10
    assert config["experiment"]["frequency_hz"] == 30


def test_load_config_accepts_string_path(experiment_config_file):
    config = load_config(str(experiment_config_file))

    assert config["experiment"]["id"] == "exp_test_001"
