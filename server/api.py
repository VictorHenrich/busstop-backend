from typing import Any, List, Union
from fastapi import FastAPI, WebSocket
import uvicorn


class ServerApi(FastAPI):
    def __init__(
        self, host: str, port: Union[int, str], *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)

        self.__host: str = host

        self.__port: Union[int, str] = port

        self.__websocket_connections: List[WebSocket] = []

    async def connect_websocket(self, websocket: WebSocket) -> None:
        await websocket.accept()

        self.__websocket_connections.append(websocket)

    async def disconnect_websocket(self, websocket: WebSocket) -> None:
        await websocket.close()

        self.__websocket_connections.remove(websocket)

    def find_websocket_connections_by_url(self, url: str) -> List[WebSocket]:
        return [
            websocket
            for websocket in self.__websocket_connections
            if url in websocket.url.path
        ]

    def start(self) -> None:
        uvicorn.run(self, host=self.__host, port=int(self.__port))
