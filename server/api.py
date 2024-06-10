from typing import Any, Union
from fastapi import FastAPI
from fastapi.routing import APIRouter
import uvicorn


class Api(FastAPI):
    def __init__(
        self, host: str, port: Union[int, str], *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)

        self.__host: str = host

        self.__port: Union[int, str] = port

        self.router = APIRouter(prefix="/api")

    def start(self) -> None:
        uvicorn.run(self, host=self.__host, port=int(self.__port))
