from server.instances import ServerInstances
from utils.responses import JSONSuccessResponse
from utils.entities import IndexEntity
from utils.config import INDEX_ENDPOINT_NAME, SWAGGER_INDEX_SESSION_TAG


@ServerInstances.general_api.get(INDEX_ENDPOINT_NAME, tags=[SWAGGER_INDEX_SESSION_TAG])
def index() -> JSONSuccessResponse[IndexEntity]:
    return JSONSuccessResponse(content=IndexEntity())
