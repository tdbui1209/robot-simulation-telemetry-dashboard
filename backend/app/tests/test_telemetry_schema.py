import pytest
from pydantic import ValidationError

from backend.app.schemas.telemetry import TelemetryPacket


def test_valid_telemetry_packet(
    valid_telemetry_packet: dict,
) -> None:
    packet = TelemetryPacket.model_validate(
        valid_telemetry_packet
    )

    assert packet.schema_version == "1.0"
    assert packet.experiment_id == "exp_walk_001"
    assert packet.run_id == "run_local_001"

    assert packet.sequence == 1
    assert packet.sim_time == pytest.approx(0.033)

    assert packet.base_pose.position.z == pytest.approx(
        0.94
    )

    assert (
        packet.base_pose.linear_velocity.vx
        == pytest.approx(0.5)
    )

    assert packet.sensors.imu.acceleration.az == pytest.approx(
        9.81
    )

    assert packet.metrics.fps == pytest.approx(30.0)


def test_missing_experiment_id_should_fail(
    valid_telemetry_packet: dict,
) -> None:
    valid_telemetry_packet.pop("experiment_id")

    with pytest.raises(ValidationError):
        TelemetryPacket.model_validate(
            valid_telemetry_packet
        )


def test_invalid_position_should_fail(
    valid_telemetry_packet: dict,
) -> None:
    valid_telemetry_packet["base_pose"]["position"]["x"] = (
        "invalid"
    )

    with pytest.raises(ValidationError):
        TelemetryPacket.model_validate(
            valid_telemetry_packet
        )


def test_event_value_is_optional(
    valid_telemetry_packet: dict,
) -> None:
    del valid_telemetry_packet["events"][0]["value"]

    packet = TelemetryPacket.model_validate(
        valid_telemetry_packet
    )

    assert packet.events[0].value is None
