from fastapi import WebSocket, WebSocketDisconnect, WebSocketException

from server.instances import ServerInstances
from utils.constants import VEHICLE_ENDPOINT_NAME


@ServerInstances.general_api.websocket(
    f"{VEHICLE_ENDPOINT_NAME}/{{vehicle_uuid}}/location"
)
async def on_connect(websocket: WebSocket, vehicle_uuid: str) -> None:
    try:
        await ServerInstances.general_api.connect_websocket(websocket)

        while True:
            await websocket.receive()

    except (WebSocketDisconnect, WebSocketException, RuntimeError):
        await ServerInstances.general_api.disconnect_websocket(websocket)
