from fastapi.routing import APIRouter

from server.instances import ServerInstances
from services.auth import AuthService
from utils.responses import JSONResponse
from utils.entities import (
    AuthResultEntity,
    AuthBodyEntity,
    AuthRefreshBodyEntity,
    AuthRefreshResultEntity,
)
from utils.constants import AUTH_ENDPOINT_NAME, SWAGGER_AUTH_SESSION_TAG


router: APIRouter = APIRouter(
    prefix=AUTH_ENDPOINT_NAME, tags=[SWAGGER_AUTH_SESSION_TAG]
)


@router.post("")
async def authenticate(body: AuthBodyEntity) -> JSONResponse[AuthResultEntity]:
    auth_service: AuthService = AuthService()

    auth_data = await auth_service.auth_agent(email=body.email, password=body.password)

    auth_body: AuthResultEntity = AuthResultEntity(
        token=auth_data["token"], refresh_token=auth_data["refresh_token"]
    )

    return JSONResponse(content=auth_body)


@router.put("/refresh")
async def refresh_authencation(
    body: AuthRefreshBodyEntity,
) -> JSONResponse[AuthRefreshResultEntity]:
    auth_service: AuthService = AuthService()

    token: str = await auth_service.refresh_token(body.refresh_token)

    auth_body: AuthRefreshResultEntity = AuthRefreshResultEntity(token=token)

    return JSONResponse(content=auth_body)


ServerInstances.api.include_router(router)
