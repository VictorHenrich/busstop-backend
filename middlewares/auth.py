from typing import Callable, Awaitable
from fastapi import Request, Response

from server.instances import ServerInstances
from models import Agent
from services.auth import AuthService
from utils.exceptions import HTTPUnauthorization
from utils.functions import validate_middleware_request


@ServerInstances.api.middleware("http")
async def verify_authentication(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
):
    verify_request = validate_middleware_request(request, call_next)

    if await anext(verify_request):
        return await anext(verify_request)

    auth_service: AuthService = AuthService()

    token: str = request.headers.get("Authorization", "")

    try:
        agent: Agent = await auth_service.get_user_data_in_token(token)

    except:
        raise HTTPUnauthorization()

    else:
        request.state.user = agent

        return await call_next(request)
