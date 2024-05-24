from typing import Any, Mapping, Optional
from fastapi.responses import JSONResponse
import json


class BaseResponseJSON(JSONResponse):
    def __init__(
        self,
        content: Any,
        status: int,
        info: str = "",
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        data: Mapping[str, Any] = {"info": info, "content": content}

        super().__init__(json.dumps(data), status, headers)


class ResponseSuccess(BaseResponseJSON):
    def __init__(
        self, content: Optional[Any] = None, headers: Mapping[str, str] | None = None
    ) -> None:
        super().__init__(content, 200, "SUCCESS", headers)


class ResponseError(BaseResponseJSON):
    def __init__(
        self, content: Optional[Any] = None, headers: Mapping[str, str] | None = None
    ) -> None:
        super().__init__(content, 500, "ERROR", headers)


class ResponseUnauthorized(BaseResponseJSON):
    def __init__(
        self, content: Optional[Any] = None, headers: Mapping[str, str] | None = None
    ) -> None:
        super().__init__(content, 404, "UNAUTHORIZED", headers)
