# Simulator

Robot/sensor telemetry generator skeleton.

Suggested responsibilities:

- Load YAML experiment config
- Generate base pose
- Generate joint states
- Generate IMU and foot contact data
- Generate runtime metrics
- Inject anomalies
- Send telemetry to backend

Suggested folders:

```text
robot_simulator/
├── config/
├── generator/
├── gait/
├── joints/
├── sensors/
├── metrics/
├── anomalies/
└── transport/
```
