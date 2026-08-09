from datetime import datetime, timezone
import math

from simulator.robot_simulator.gait import gait_phase
from simulator.robot_simulator.sensors import generate_sensors
from simulator.robot_simulator.metrics import generate_metrics
from simulator.robot_simulator.anomalies import anomaly_flags, build_event


class TelemetryGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.sequence = 0
        self.sim_time = 0.0
        self.dt = 1.0 / config["experiment"]["frequency_hz"]

    def next_packet(self) -> dict:
        exp = self.config["experiment"]
        robot = self.config["robot"]
        motion = self.config["motion"]
        noise = self.config["noise"]
        flags = anomaly_flags(self.config)

        if flags.get("packet_drop"):
            self.sequence += 2
        else:
            self.sequence += 1

        self.sim_time += self.dt

        left_phase, right_phase = gait_phase(self.sim_time, motion["gait_frequency_hz"])
        target = motion["target_velocity"]
        mode = motion["mode"]

        x = target["vx"] * self.sim_time
        y = motion["lateral_sway_m"] * math.sin(left_phase)
        z = robot["base_height_m"] + motion["vertical_bob_m"] * math.sin(2 * left_phase)

        roll_factor = motion["roll_factor_std"] if mode == "unstable_walk" else motion["roll_factor_std"] / 2
        pitch_factor = motion["pitch_factor_std"] if mode == "unstable_walk" else motion["pitch_factor_std"] / 2
        roll = roll_factor * math.sin(left_phase)
        pitch = pitch_factor * math.sin(left_phase + math.pi / 3)
        yaw = target["yaw_rate"] * self.sim_time

        sensors = generate_sensors(
            left_phase,
            right_phase,
            robot["mass_kg"],
            noise["imu_accel_std"],
            noise["gyro_std"],
            noise["foot_force_std_n"],
        )

        actual_vx = target["vx"] + 0.02 * math.sin(left_phase)
        tracking_error = abs(target["vx"] - actual_vx)
        metrics = generate_metrics(
            exp["frequency_hz"],
            self.dt * 1000,
            noise["latency_std_ms"],
            roll,
            pitch,
            tracking_error,
            latency_spike=flags.get("latency_spike", False),
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
                "position": {"x": x, "y": y, "z": z},
                "orientation": {"roll": roll, "pitch": pitch, "yaw": yaw},
                "linear_velocity": {"vx": actual_vx, "vy": 0.0, "vz": 0.0},
                "angular_velocity": {"wx": roll, "wy": pitch, "wz": target["yaw_rate"]}
            },
            "sensors": sensors,
            "control_command": {
                "mode": mode,
                "target_velocity": target,
            },
            "metrics": metrics,
            "events": build_event(flags, metrics),
        }
