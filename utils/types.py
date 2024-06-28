from typing import TypeAlias, Union
from utils.responses import JSONErrorResponse, JSONSuccessResponse

JSONResponseType: TypeAlias = Union[JSONSuccessResponse, JSONErrorResponse]
