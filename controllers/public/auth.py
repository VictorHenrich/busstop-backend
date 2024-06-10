from server.instances import ServerInstances
from services.auth import AuthService
from utils.responses import JSONResponse
from utils.entities import (
    AuthResultEntity,
    AuthBodyEntity,
    AuthRefreshBodyEntity,
    AuthRefreshResultEntity,
)
from utils.constants import AUTH_ENDPOINT_NAME


@ServerInstances.public_api.post(AUTH_ENDPOINT_NAME)
async def authenticate(body: AuthBodyEntity) -> JSONResponse[AuthResultEntity]:
    auth_service: AuthService = AuthService()

    auth_data = await auth_service.auth_agent(email=body.email, password=body.password)

    auth_body: AuthResultEntity = AuthResultEntity(
        token=auth_data["token"], refresh_token=auth_data["refresh_token"]
    )

    return JSONResponse(content=auth_body)


@ServerInstances.public_api.put(f"{AUTH_ENDPOINT_NAME}/refresh")
async def refresh_authencation(
    body: AuthRefreshBodyEntity,
) -> JSONResponse[AuthRefreshResultEntity]:
    auth_service: AuthService = AuthService()

    token: str = await auth_service.refresh_token(body.refresh_token)

    auth_body: AuthRefreshResultEntity = AuthRefreshResultEntity(token=token)

    return JSONResponse(content=auth_body)
