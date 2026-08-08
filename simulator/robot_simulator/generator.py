from datetime import datetime, timezone


class TelemetryGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.sequence = 0
        self.sim_time = 0.0
        self.dt = 1.0 / config["experiment"]["frequency_hz"]

    def next_packet(self):
        exp = self.config["experiment"]

        self.sim_time += self.dt

        return {
            "schema_version": "1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "experiment_id": exp["id"],
            "run_id": exp["run_id"],
            "robot_id": exp["robot_id"],
            "sequence": self.sequence,
            "sim_time": self.sim_time
        }
