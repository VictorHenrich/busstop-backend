from fastapi.routing import APIRouter
import jwt

from server.instances import ServerInstances
from services.auth import AuthService
from utils.responses import JSONSuccessResponse
from utils.entities import (
    AuthResultEntity,
    AuthBodyEntity,
    AuthRefreshBodyEntity,
    AuthRefreshResultEntity,
)
from utils.constants import AUTH_ENDPOINT_NAME, SWAGGER_AUTH_SESSION_TAG
from utils.exceptions import (
    InvalidToken,
    UserNotFound,
    InvalidUserPassword,
    HTTPFailure,
)


router: APIRouter = APIRouter(
    prefix=AUTH_ENDPOINT_NAME, tags=[SWAGGER_AUTH_SESSION_TAG]
)


@router.post("")
async def authenticate(body: AuthBodyEntity) -> JSONSuccessResponse[AuthResultEntity]:
    auth_service: AuthService = AuthService()

    try:
        auth_data = await auth_service.auth_agent(
            email=body.email, password=body.password
        )

    except (
        UserNotFound,
        InvalidUserPassword,
    ) as error:
        raise HTTPFailure(str(error))

    auth_body: AuthResultEntity = AuthResultEntity(
        token=auth_data["token"], refresh_token=auth_data["refresh_token"]
    )

    return JSONSuccessResponse(content=auth_body)


@router.put("/refresh")
async def refresh_authencation(
    body: AuthRefreshBodyEntity,
) -> JSONSuccessResponse[AuthRefreshResultEntity]:
    auth_service: AuthService = AuthService()

    try:
        token: str = await auth_service.refresh_token(body.refresh_token)

        auth_body: AuthRefreshResultEntity = AuthRefreshResultEntity(token=token)

    except (InvalidToken, jwt.ExpiredSignatureError, jwt.DecodeError) as error:
        raise HTTPFailure(str(error))

    else:
        return JSONSuccessResponse(content=auth_body)


ServerInstances.api.include_router(router)
