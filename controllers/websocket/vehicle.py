from fastapi import WebSocket

from server.instances import ServerInstances
from utils.constants import VEHICLE_ENDPOINT_NAME


@ServerInstances.general_api.websocket(f"{VEHICLE_ENDPOINT_NAME}/location")
async def on_connect(websocket: WebSocket) -> None:
    await ServerInstances.general_api.connect_websocket(websocket)
