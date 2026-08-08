# Robot Simulation Telemetry Dashboard

Basic repository skeleton for a robotics simulation telemetry platform project.

## Purpose

This project is intended to demonstrate the software platform layer around robotics simulation:

- Experiment configuration
- Robot/sensor telemetry streaming
- Backend telemetry ingestion
- JSONL logging
- Experiment listing and replay
- Real-time dashboard visualization

This repository intentionally starts as a basic skeleton without implementation code.

## Proposed Runtime Flow

```text
Robot Simulator -> Backend Ingestion -> JSONL Logs -> Replay API -> Dashboard
```

## Main Modules

```text
simulator/  - robot/sensor state generator
backend/    - API, telemetry ingestion, logging, replay
frontend/   - real-time dashboard
configs/    - YAML experiment configs
docs/       - architecture and design notes
logs/       - generated JSONL logs, not committed
samples/    - sample packets, screenshots, summaries
scripts/    - local helper scripts
```

## Suggested Milestones

### Milestone 1: Simulator MVP

- Define telemetry schema
- Define YAML experiment config
- Generate one telemetry packet
- Print packets to console

### Milestone 2: Backend MVP

- Add telemetry ingestion endpoint
- Validate packet schema
- Save JSONL logs
- Expose health endpoint

### Milestone 3: Dashboard MVP

- Connect to backend
- Show latest telemetry packet
- Show key metrics

### Milestone 4: Replay

- List experiments
- Load JSONL logs
- Replay packets by `sim_time`

## Suggested Tech Stack

- Backend: FastAPI
- Simulator: Python
- Frontend: React
- Logging: JSONL
- Config: YAML
- Optional future extensions: UDP bridge, MuJoCo, Three.js, ROS2
