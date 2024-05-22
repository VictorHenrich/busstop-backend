from typing import Any, Union
from fastapi import FastAPI
import uvicorn


class Api(FastAPI):
    def __init__(
        self, host: str, port: Union[int, str], *args: Any, **kwargs: Any
    ) -> None:
        self.__host: str = host

        self.__port: Union[int, str] = port

        super().__init__(*args, **kwargs)

    def start(self) -> None:
        uvicorn.run(self, host=self.__host, port=int(self.__port))
