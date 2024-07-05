from typing import Optional
from fastapi.routing import APIRouter

from server.instances import ServerInstances
from services.user import UserService
from models import User
from utils.responses import JSONSuccessResponse
from utils.entities import UserBodyEntity, UserEntity
from utils.constants import USER_ENDPOINT_NAME, SWAGGER_USER_SESSION_TAG
from utils.functions import get_user_entity, handle_user_body


router: APIRouter = APIRouter(
    prefix=USER_ENDPOINT_NAME, tags=[SWAGGER_USER_SESSION_TAG]
)


@router.get("/{user_uuid}")
async def find_user(user_uuid: str) -> JSONSuccessResponse[UserEntity]:
    user_service: UserService = UserService()

    user: User = await user_service.find_user(user_uuid)

    user_handled: UserEntity = get_user_entity(user)

    return JSONSuccessResponse(content=user_handled)


@router.post("")
async def create_user(
    body: UserBodyEntity,
) -> JSONSuccessResponse[Optional[UserEntity]]:
    user_service: UserService = UserService()

    user: Optional[User] = await user_service.create_user(
        name=body.name, email=body.email, password=body.password
    )

    user_handled: Optional[UserEntity] = handle_user_body(user)

    return JSONSuccessResponse(content=user_handled)


@router.put("/{user_uuid}")
async def update_user(
    user_uuid: str, body: UserBodyEntity
) -> JSONSuccessResponse[Optional[UserEntity]]:
    user_service: UserService = UserService()

    user: Optional[User] = await user_service.update_user(
        user_uuid=user_uuid, name=body.name, email=body.email, password=body.password
    )

    user_handled: Optional[UserEntity] = handle_user_body(user)

    return JSONSuccessResponse(content=user_handled)


@router.delete("/{user_uuid}")
async def delete_user(user_uuid: str) -> JSONSuccessResponse[Optional[UserEntity]]:
    user_service: UserService = UserService()

    user: Optional[User] = await user_service.delete_user(
        user_uuid=user_uuid,
    )

    user_handled: Optional[UserEntity] = handle_user_body(user)

    return JSONSuccessResponse(content=user_handled)


ServerInstances.api.include_router(router)
