from server.instances import ServerInstances
from utils.responses import SuccessJSONResponse, JSONBaseResponse
from utils.entities import IndexEntity


@ServerInstances.api.get("/")
def index() -> JSONBaseResponse[IndexEntity]:
    return SuccessJSONResponse(content=IndexEntity())
