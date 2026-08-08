import argparse
import asyncio
from pathlib import Path
import random

import yaml

from simulator.robot_simulator.generator import TelemetryGenerator


def load_config(path: str | Path) -> dict:
    with Path(str(path)).open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    random.seed(config["experiment"].get("random_state", 42))
    return config


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    generator = TelemetryGenerator(config)

    hz = config["experiment"]["frequency_hz"]
    duration = config["experiment"]["duration_sec"]
    sleep_sec = 1.0 / hz
    total_steps = int(duration * hz)

    for _ in range(total_steps):
        packet = generator.next_packet()
        try:
            print(f"seq={packet['sequence']} sim_time={packet['sim_time']:.3f}")
        except Exception as exc:
            print(f"failed to send telemetry: {exc}")
        print(f"sleeping: {sleep_sec}s\n")


if __name__ == "__main__":
    asyncio.run(main())
