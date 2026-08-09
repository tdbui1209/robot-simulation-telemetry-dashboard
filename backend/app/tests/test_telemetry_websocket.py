from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_websocket_accepts_valid_packet(
    valid_telemetry_packet: dict,
) -> None:
    with client.websocket_connect(
        "/ws/telemetry"
    ) as websocket:

        websocket.send_json(
            valid_telemetry_packet
        )

        response = websocket.receive_json()

        assert response["type"] == "ack"
        assert response["sequence"] == 1


def test_websocket_rejects_invalid_packet(
    valid_telemetry_packet: dict,
) -> None:

    valid_telemetry_packet.pop("robot_id")

    with client.websocket_connect(
        "/ws/telemetry"
    ) as websocket:

        websocket.send_json(
            valid_telemetry_packet
        )

        response = websocket.receive_json()

        assert response["type"] == "error"
        assert (
            response["error"]
            == "invalid_telemetry"
        )

        assert "detail" in response


def test_invalid_packet_reports_field(
    valid_telemetry_packet: dict,
) -> None:

    valid_telemetry_packet.pop("robot_id")

    with client.websocket_connect(
        "/ws/telemetry"
    ) as websocket:

        websocket.send_json(
            valid_telemetry_packet
        )

        response = websocket.receive_json()

        errors = response["detail"]

        assert any(
            error["loc"] == ["robot_id"]
            for error in errors
        )


def test_websocket_stays_connected_after_invalid_packet(
    valid_telemetry_packet: dict,
) -> None:

    with client.websocket_connect(
        "/ws/telemetry"
    ) as websocket:

        invalid_packet = (
            valid_telemetry_packet.copy()
        )

        invalid_packet.pop("robot_id")

        websocket.send_json(
            invalid_packet
        )

        error_response = websocket.receive_json()

        assert error_response["type"] == "error"

        websocket.send_json(
            valid_telemetry_packet
        )

        ack_response = websocket.receive_json()

        assert ack_response == {
            "type": "ack",
            "sequence": 1,
        }
