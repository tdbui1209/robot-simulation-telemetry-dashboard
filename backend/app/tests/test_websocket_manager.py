import pytest

from backend.app.streaming.websocket_manager import WebSocketManager


class FakeWebSocket:
    def __init__(self) -> None:
        self.accepted = False
        self.messages: list[dict] = []

    async def accept(self) -> None:
        self.accepted = True

    async def send_json(self, data: dict,) -> None:
        self.messages.append(data)


@pytest.mark.asyncio
async def test_connect() -> None:
    manager = WebSocketManager()

    websocket = FakeWebSocket()

    await manager.connect(websocket)

    assert websocket.accepted is True
    assert websocket in manager.active_connections


@pytest.mark.asyncio
async def test_disconnect() -> None:
    manager = WebSocketManager()

    websocket = FakeWebSocket()

    await manager.connect(websocket)

    manager.disconnect(websocket)

    assert websocket not in manager.active_connections


@pytest.mark.asyncio
async def test_broadcast_json() -> None:
    manager = WebSocketManager()

    websocket_1 = FakeWebSocket()
    websocket_2 = FakeWebSocket()

    await manager.connect(websocket_1)
    await manager.connect(websocket_2)

    data = {
        "type": "telemetry",
        "data": {
            "sequence": 1,
        },
    }

    await manager.broadcast_json(data)

    assert websocket_1.messages == [data]
    assert websocket_2.messages == [data]


class BrokenWebSocket(FakeWebSocket):

    async def send_json(self, data: dict) -> None:
        raise RuntimeError("connection closed")


@pytest.mark.asyncio
async def test_broadcast_removes_dead_connection() -> None:
    manager = WebSocketManager()

    good_ws = FakeWebSocket()
    broken_ws = BrokenWebSocket()

    await manager.connect(good_ws)
    await manager.connect(broken_ws)

    data = {
        "type": "telemetry"
    }

    await manager.broadcast_json(data)

    assert good_ws in manager.active_connections
    assert broken_ws not in manager.active_connections
    assert good_ws.messages == [data]


def test_disconnect_unknown_websocket() -> None:
    manager = WebSocketManager()

    websocket = FakeWebSocket()

    manager.disconnect(websocket)

    assert len(manager.active_connections) == 0
