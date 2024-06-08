from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from copy import copy

from models import Company, database, Agent
from repositories.agent import (
    AgentRepository,
    AgentCreationRepositoryProps,
    AgentUpdateRepositoryProps,
    AgentExclusionRepositoryProps,
    AgentCaptureRepositoryProps,
    AgentListingRepositoryProps,
    AgentAuthRepositoryProps,
)
from services.company import CompanyService
from utils.patterns import AbstractBaseEntity
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


class AgentAuthProps(AbstractBaseEntity):
    email: str

    password: str


class AgentService:
    def __init__(self) -> None:
        self.__session: AsyncSession = database.create_async_session()

        self.__agent_repository: AgentRepository = AgentRepository(self.__session)

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
        async with self.__session:
            company: Company = await self.__get_company(company_uuid, company_instance)

            agent_props: AgentCreationRepositoryProps = AgentCreationProps(
                company=company,
                name=name,
                email=email,
                password=password,
            )

            agent: Optional[Agent] = await self.__agent_repository.create(agent_props)

            await self.__session.commit()

            return agent

    async def update_agent(
        self,
        agent_uuid: str,
        name: str,
        email: str,
        password: str,
        agent_instance: Optional[Agent] = None,
    ) -> Optional[Agent]:
        async with self.__session:
            agent_props: AgentUpdateRepositoryProps = AgentUpdateProps(
                uuid=agent_uuid,
                name=name,
                email=email,
                password=password,
                instance=agent_instance,
            )

            agent: Optional[Agent] = await self.__agent_repository.update(agent_props)

            await self.__session.commit()

            if agent is not None:
                await self.__session.refresh(agent)

            return agent

    async def delete_agent(
        self, agent_uuid: str, agent_instance: Optional[Agent] = None
    ) -> Optional[Agent]:
        async with self.__session:
            agent_props: AgentExclusionRepositoryProps = AgentExclusionProps(
                uuid=agent_uuid, instance=agent_instance
            )

            agent: Optional[Agent] = await self.__agent_repository.delete(agent_props)

            if agent is not None:
                return copy(agent)

    async def find_agent(self, agent_uuid: str) -> Agent:
        async with self.__session:
            agent_props: AgentCaptureRepositoryProps = AgentCaptureProps(
                uuid=agent_uuid
            )

            agent: Optional[Agent] = await self.__agent_repository.find(agent_props)

            if agent is None:
                raise ModelNotFound(Agent, agent_uuid)

            return agent

    async def find_agents(
        self,
        company_uuid: Optional[str] = None,
        company_instance: Optional[Company] = None,
    ) -> Sequence[Agent]:
        async with self.__session:
            company: Company = await self.__get_company(company_uuid, company_instance)

            agent_props: AgentListingRepositoryProps = AgentListingProps(
                company=company
            )

            return await self.__agent_repository.find_many(agent_props)

    async def auth_agent(self, email: str, password: str) -> Agent:
        async with self.__session:
            agent_props: AgentAuthRepositoryProps = AgentAuthProps(
                email=email, password=password
            )

            return await self.__agent_repository.auth(agent_props)
