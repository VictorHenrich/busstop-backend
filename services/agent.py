from typing import Optional, Sequence
from copy import copy

from models import Company, database, Agent
from repositories.agent import (
    AgentRepository,
    IAgentCreateRepository,
    IAgentUpdateRepository,
    IAgentExclusionRepository,
    IAgentFindRepository,
    IAgentFindManyRepository,
)
from services.company import CompanyService
from utils.patterns import (
    AbstractBaseEntity,
    ICreateRepository,
    IDeleteRepository,
    IFindManyRepository,
    IFindRepository,
    IUpdateRepository,
)
from utils.exceptions import ModelNotFound


class AgentCreationProps(AbstractBaseEntity):
    name: str

    email: str

    password: str

    company: Company


class AgentUpdateProps(AbstractBaseEntity):
    uuid: str

    name: str

    email: str

    password: str

    instance: Optional[Agent]


class AgentExclusionProps(AbstractBaseEntity):
    uuid: str
    instance: Optional[Agent]


class AgentCaptureProps(AbstractBaseEntity):
    uuid: str


class AgentListingProps(AbstractBaseEntity):
    company: Company


class AgentService:
    def __init__(self) -> None:
        self.__company_service: CompanyService = CompanyService()

    async def __get_company(
        self, company_uuid: Optional[str], company_instance: Optional[Company]
    ):
        if company_instance is None:
            return await self.__company_service.find_company(company_uuid or "")

        else:
            return company_instance

    async def create_agent(
        self,
        name: str,
        email: str,
        password: str,
        company_uuid: Optional[str] = None,
        company_instance: Optional[Company] = None,
    ) -> Optional[Agent]:
        async with database.create_async_session() as session:
            agent_repository: ICreateRepository[
                IAgentCreateRepository, Optional[Agent]
            ] = AgentRepository(session)

            company: Company = await self.__get_company(company_uuid, company_instance)

            agent_props: IAgentCreateRepository = AgentCreationProps(
                company=company,
                name=name,
                email=email,
                password=password,
            )

            agent: Optional[Agent] = await agent_repository.create(agent_props)

            await session.commit()

            return agent

    async def update_agent(
        self,
        agent_uuid: str,
        name: str,
        email: str,
        password: str,
        agent_instance: Optional[Agent] = None,
    ) -> Optional[Agent]:
        async with database.create_async_session() as session:
            agent_repository: IUpdateRepository[
                IAgentUpdateRepository, Optional[Agent]
            ] = AgentRepository(session)

            agent_props: IAgentUpdateRepository = AgentUpdateProps(
                uuid=agent_uuid,
                name=name,
                email=email,
                password=password,
                instance=agent_instance,
            )

            agent: Optional[Agent] = await agent_repository.update(agent_props)

            await session.commit()

            if agent is not None:
                await session.refresh(agent)

            return agent

    async def delete_agent(
        self, agent_uuid: str, agent_instance: Optional[Agent] = None
    ) -> Optional[Agent]:
        async with database.create_async_session() as session:
            agent_repository: IDeleteRepository[
                IAgentExclusionRepository, Optional[Agent]
            ] = AgentRepository(session)

            agent_props: IAgentExclusionRepository = AgentExclusionProps(
                uuid=agent_uuid, instance=agent_instance
            )

            agent: Optional[Agent] = await agent_repository.delete(agent_props)

            await session.commit()

            if agent is not None:
                return copy(agent)

    async def find_agent(self, agent_uuid: str) -> Agent:
        async with database.create_async_session() as session:
            agent_repository: IFindRepository[
                IAgentFindRepository, Agent
            ] = AgentRepository(session)

            agent_props: IAgentFindRepository = AgentCaptureProps(uuid=agent_uuid)

            agent: Optional[Agent] = await agent_repository.find(agent_props)

            if agent is None:
                raise ModelNotFound(Agent, agent_uuid)

            return agent

    async def find_agents(
        self,
        company_uuid: Optional[str] = None,
        company_instance: Optional[Company] = None,
    ) -> Sequence[Agent]:
        async with database.create_async_session() as session:
            agent_repository: IFindManyRepository[
                IAgentFindManyRepository, Agent
            ] = AgentRepository(session)

            company: Company = await self.__get_company(company_uuid, company_instance)

            agent_props: IAgentFindManyRepository = AgentListingProps(company=company)

            return await agent_repository.find_many(agent_props)
