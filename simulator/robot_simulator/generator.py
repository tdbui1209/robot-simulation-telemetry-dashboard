from datetime import datetime, timezone

from simulator.robot_simulator.gait import gait_phase
from simulator.robot_simulator.sensors import generate_sensors


class TelemetryGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.sequence = 0
        self.sim_time = 0.0
        self.dt = 1.0 / config["experiment"]["frequency_hz"]

    def next_packet(self):
        exp = self.config["experiment"]
        robot = self.config["robot"]
        motion = self.config["motion"]

        self.sim_time += self.dt

        left_phase, right_phase = gait_phase(self.sim_time, motion["gait_frequency_hz"])
        target = motion["target_velocity"]
        mode = motion["mode"]

        x = target["vx"] * self.sim_time
        y = 0
        z = robot["base_height_m"]

        sensors = generate_sensors(
            left_phase,
            right_phase,
            robot["mass_kg"],
        )

        return {
            "schema_version": "1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "experiment_id": exp["id"],
            "run_id": exp["run_id"],
            "robot_id": exp["robot_id"],
            "sequence": self.sequence,
            "sim_time": self.sim_time,
            "base_pose": {
                "position": {"x": x, "y": y, "z": z}
            },
            "sensors": sensors,
            "control_command": {
                "mode": mode,
            }
        }
