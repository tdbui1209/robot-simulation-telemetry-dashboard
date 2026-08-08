# Architecture

## Goal

Design a small robotics simulation platform that can receive robot-like telemetry, persist logs, and support replay/debugging.

## Proposed Flow

```text
Simulator -> Backend -> JSONL Storage -> Replay API -> Dashboard
```

## Control Plane

Responsible for:

- Experiment config
- Experiment metadata
- Start/stop run lifecycle
- Summary and replay requests

## Data Plane

Responsible for:

- High-frequency robot telemetry
- Base pose
- Joint states
- Sensor data
- Runtime metrics
- Events and anomalies

## Future Extensions

- UDP telemetry bridge
- MuJoCo integration
- Three.js visualization
- ROS2 bridge
