from server.instances import ServerInstances
from utils.responses import SuccessJSONResponse
from utils.entities import JSONDataEntity, IndexEntity


@ServerInstances.api.get("/")
def index() -> JSONDataEntity[IndexEntity]:
    return SuccessJSONResponse(content=IndexEntity())
