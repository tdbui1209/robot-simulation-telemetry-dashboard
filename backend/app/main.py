from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from backend.app.schemas.telemetry import TelemetryPacket
from backend.app.streaming.websocket_manager import websocket_manager


app = FastAPI(title="Robot Simulation Telemetry Dashboard")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.websocket("/ws/telemetry")
async def telemetry_ws(websocket: WebSocket) -> None:
    await websocket.accept()

    try:
        while True:
            raw_packet = await websocket.receive_json()

            try:
                packet = TelemetryPacket.model_validate(
                    raw_packet
                )

            except ValidationError as exc:
                await websocket.send_json(
                    {
                        "type": "error",
                        "error": "invalid_telemetry",
                        "detail": exc.errors(),
                    }
                )
                continue

            packet_dict = packet.model_dump(mode="json")

            await websocket_manager.broadcast_json(
                {
                    "type": "telemetry",
                    "data": packet_dict,
                }
            )

    except WebSocketDisconnect:
        pass
