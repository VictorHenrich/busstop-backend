from typing import Callable
from fastapi import Request

from server.instances import ServerInstances
from models import Agent
from services.auth import AuthService
from utils.exceptions import HTTPUnauthorization


@ServerInstances.api.middleware("http")
async def verify_authentication(request: Request, call_next: Callable):
    auth_service: AuthService = AuthService()

    token: str = request.headers["Authorization"]

    try:
        agent: Agent = await auth_service.get_user_data_in_token(token)

    except:
        raise HTTPUnauthorization()

    else:
        request.state.user = agent

        call_next(request)
