from server.instances import ServerInstances
from utils.responses import JSONResponse
from utils.entities import IndexEntity


@ServerInstances.api.get("/")
def index() -> JSONResponse[IndexEntity]:
    return JSONResponse(content=IndexEntity())
