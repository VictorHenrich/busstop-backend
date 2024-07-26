from fastapi import WebSocket, WebSocketDisconnect, WebSocketException

from server.instances import ServerInstances
from utils.constants import VEHICLE_ENDPOINT_NAME


@ServerInstances.general_api.websocket(f"{VEHICLE_ENDPOINT_NAME}/location")
async def on_connect(websocket: WebSocket) -> None:
    try:
        await ServerInstances.general_api.connect_websocket(websocket)

        while True:
            await websocket.receive()

    except (WebSocketDisconnect, WebSocketException):
        await ServerInstances.general_api.disconnect_websocket(websocket)
