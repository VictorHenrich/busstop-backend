from typing import Sequence, Optional, List
from fastapi.routing import APIRouter
from fastapi import Request

from server.instances import ServerInstances
from services.agent import AgentService
from models import Agent, Company
from utils.responses import JSONSuccessResponse
from utils.entities import AgentBodyEntity, AgentEntity
from utils.config import PROFILE_ENDPOINT_NAME, SWAGGER_PROFILE_SESSION_TAG
from utils.functions import get_agent_entity, handle_agent_body


router: APIRouter = APIRouter(
    prefix=PROFILE_ENDPOINT_NAME, tags=[SWAGGER_PROFILE_SESSION_TAG]
)


@router.get("/{agent_uuid}")
async def find_agent(agent_uuid: str) -> JSONSuccessResponse[AgentEntity]:
    agent_service: AgentService = AgentService()

    agent: Agent = await agent_service.find_agent(agent_uuid)

    agent_handled: AgentEntity = get_agent_entity(agent)

    return JSONSuccessResponse(content=agent_handled)


@router.get("")
async def find_agents(request: Request) -> JSONSuccessResponse[List[AgentEntity]]:
    company: Company = request.state.user.company

    agent_service: AgentService = AgentService()

    agents: Sequence[Agent] = await agent_service.find_agents(company_instance=company)

    agents_handled: List[AgentEntity] = [get_agent_entity(agent) for agent in agents]

    return JSONSuccessResponse(content=agents_handled)


@router.post("")
async def create_agent(
    request: Request, body: AgentBodyEntity
) -> JSONSuccessResponse[Optional[AgentEntity]]:
    company: Company = request.state.user.company

    agent_service: AgentService = AgentService()

    agent: Optional[Agent] = await agent_service.create_agent(
        company_instance=company,
        name=body.name,
        email=body.email,
        password=body.password,
    )

    agent_handled: Optional[AgentEntity] = handle_agent_body(agent)

    return JSONSuccessResponse(content=agent_handled)


@router.put("/{agent_uuid}")
async def update_agent(
    agent_uuid: str, body: AgentBodyEntity
) -> JSONSuccessResponse[Optional[AgentEntity]]:
    agent_service: AgentService = AgentService()

    agent: Optional[Agent] = await agent_service.update_agent(
        agent_uuid=agent_uuid, name=body.name, email=body.email, password=body.password
    )

    agent_handled: Optional[AgentEntity] = handle_agent_body(agent)

    return JSONSuccessResponse(content=agent_handled)


@router.delete("/{agent_uuid}")
async def delete_agent(agent_uuid: str) -> JSONSuccessResponse[Optional[AgentEntity]]:
    agent_service: AgentService = AgentService()

    agent: Optional[Agent] = await agent_service.delete_agent(
        agent_uuid=agent_uuid,
    )

    agent_handled: Optional[AgentEntity] = handle_agent_body(agent)

    return JSONSuccessResponse(content=agent_handled)


ServerInstances.agent_api.include_router(router)
