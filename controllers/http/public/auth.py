from fastapi.routing import APIRouter
import jwt

from server.instances import ServerInstances
from services.auth import AuthService, AuthResult
from utils.responses import JSONSuccessResponse
from utils.entities import (
    AuthResultEntity,
    AuthBodyEntity,
    AuthRefreshBodyEntity,
    AuthRefreshResultEntity,
)
from utils.config import AUTH_ENDPOINT_NAME, SWAGGER_AUTH_SESSION_TAG
from utils.exceptions import (
    InvalidToken,
    UserNotFound,
    InvalidUserPassword,
    HTTPFailure,
)


agent_router: APIRouter = APIRouter(
    prefix=AUTH_ENDPOINT_NAME, tags=[SWAGGER_AUTH_SESSION_TAG]
)

user_router: APIRouter = APIRouter(
    prefix=AUTH_ENDPOINT_NAME, tags=[SWAGGER_AUTH_SESSION_TAG]
)


@agent_router.post("")
async def authenticate_agent(
    body: AuthBodyEntity,
) -> JSONSuccessResponse[AuthResultEntity]:
    auth_service: AuthService = AuthService()

    try:
        auth_data: AuthResult = await auth_service.auth_agent(
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


@agent_router.put("/refresh")
async def refresh_agent_authencation(
    body: AuthRefreshBodyEntity,
) -> JSONSuccessResponse[AuthRefreshResultEntity]:
    auth_service: AuthService = AuthService()

    try:
        token: str = await auth_service.refresh_agent_token(body.refresh_token)

        auth_body: AuthRefreshResultEntity = AuthRefreshResultEntity(token=token)

    except (InvalidToken, jwt.ExpiredSignatureError, jwt.DecodeError) as error:
        raise HTTPFailure(str(error))

    else:
        return JSONSuccessResponse(content=auth_body)


@user_router.post("")
async def authenticate_user(
    body: AuthBodyEntity,
) -> JSONSuccessResponse[AuthResultEntity]:
    auth_service: AuthService = AuthService()

    try:
        auth_data: AuthResult = await auth_service.auth_user(
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


@user_router.put("/refresh")
async def refresh_user_authencation(
    body: AuthRefreshBodyEntity,
) -> JSONSuccessResponse[AuthRefreshResultEntity]:
    auth_service: AuthService = AuthService()

    try:
        token: str = await auth_service.refresh_user_token(body.refresh_token)

        auth_body: AuthRefreshResultEntity = AuthRefreshResultEntity(token=token)

    except (InvalidToken, jwt.ExpiredSignatureError, jwt.DecodeError) as error:
        raise HTTPFailure(str(error))

    else:
        return JSONSuccessResponse(content=auth_body)


ServerInstances.agent_api.include_router(agent_router)

ServerInstances.user_api.include_router(user_router)
