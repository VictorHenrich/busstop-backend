from typing import Sequence, Optional, List

from server.instances import ServerInstances
from services.agent import AgentService
from models import Agent
from utils.responses import JSONResponse
from utils.entities import AgentBodyEntity, AgentEntity
from utils.constants import AGENT_ENDPOINT_NAME
from utils.functions import get_agent_entity, handle_agent_body


@ServerInstances.private_api.get(f"{AGENT_ENDPOINT_NAME}/{{agent_uuid}}")
async def find_agent(agent_uuid: str) -> JSONResponse[AgentEntity]:
    agent_service: AgentService = AgentService()

    agent: Agent = await agent_service.find_agent(agent_uuid)

    agent_handled: AgentEntity = get_agent_entity(agent)

    return JSONResponse(content=agent_handled)


@ServerInstances.private_api.get(AGENT_ENDPOINT_NAME)
async def find_agents() -> JSONResponse[List[AgentEntity]]:
    agent_service: AgentService = AgentService()

    agents: Sequence[Agent] = await agent_service.find_agents()

    agents_handled: List[AgentEntity] = [get_agent_entity(agent) for agent in agents]

    return JSONResponse(content=agents_handled)


@ServerInstances.private_api.post(AGENT_ENDPOINT_NAME)
async def create_agent(body: AgentBodyEntity) -> JSONResponse[Optional[AgentEntity]]:
    agent_service: AgentService = AgentService()

    agent: Optional[Agent] = await agent_service.create_agent(
        name=body.name, email=body.email, password=body.password
    )

    agent_handled: Optional[AgentEntity] = handle_agent_body(agent)

    return JSONResponse(content=agent_handled)


@ServerInstances.private_api.put(f"{AGENT_ENDPOINT_NAME}/{{agent_uuid}}")
async def update_agent(
    agent_uuid: str, body: AgentBodyEntity
) -> JSONResponse[Optional[AgentEntity]]:
    agent_service: AgentService = AgentService()

    agent: Optional[Agent] = await agent_service.update_agent(
        agent_uuid=agent_uuid, name=body.name, email=body.email, password=body.password
    )

    agent_handled: Optional[AgentEntity] = handle_agent_body(agent)

    return JSONResponse(content=agent_handled)


@ServerInstances.private_api.delete(f"{AGENT_ENDPOINT_NAME}/{{agent_uuid}}")
async def delete_agent(agent_uuid: str) -> JSONResponse[Optional[AgentEntity]]:
    agent_service: AgentService = AgentService()

    agent: Optional[Agent] = await agent_service.delete_agent(
        agent_uuid=agent_uuid,
    )

    agent_handled: Optional[AgentEntity] = handle_agent_body(agent)

    return JSONResponse(content=agent_handled)
