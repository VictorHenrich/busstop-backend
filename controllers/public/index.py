from server.instances import ServerInstances
from utils.responses import JSONSuccessResponse
from utils.entities import IndexEntity
from utils.constants import INDEX_ENDPOINT_NAME, SWAGGER_INDEX_SESSION_TAG


@ServerInstances.api.get(INDEX_ENDPOINT_NAME, tags=[SWAGGER_INDEX_SESSION_TAG])
def index() -> JSONSuccessResponse[IndexEntity]:
    return JSONSuccessResponse(content=IndexEntity())
