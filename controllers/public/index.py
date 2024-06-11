from server.instances import ServerInstances
from utils.responses import JSONResponse
from utils.entities import IndexEntity
from utils.constants import INDEX_ENDPOINT_NAME


@ServerInstances.api.get(INDEX_ENDPOINT_NAME)
def index() -> JSONResponse[IndexEntity]:
    return JSONResponse(content=IndexEntity())
