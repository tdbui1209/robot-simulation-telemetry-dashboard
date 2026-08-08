# Replay Design

Recommended approach:

1. Save each telemetry packet as one JSONL line.
2. Use `sim_time` as logical playback time.
3. Allow replay speed such as 0.5x, 1x, 2x.
4. Support filtering by event type or time range.
5. Do not load large logs fully into memory in production design.
