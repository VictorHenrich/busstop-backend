from typing import Optional, Sequence
from unittest.mock import Mock
import logging

from models import Agent, Company, database
from repositories.agent import (
    AgentRepository,
    IAgentCreateRepository,
    IAgentUpdateRepository,
    IAgentDeleteRepository,
    IAgentFindRepository,
    IAgentFindManyRepository,
    IAgentAuthRepository,
)
from tests.repositories.mocks import create_company
from utils.patterns import (
    IAuthRepository,
    ICreateRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindRepository,
    IFindManyRepository,
)
from .mocks import create_company, create_agent
from .common import BaseRepositoryTestCase


class AgentRepositoryOnlineTestCase(BaseRepositoryTestCase):
    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()

        self.__agent_email: str = "user_test@gmail.com"

        self.__agent_password: str = "1234"

        self.company: Company = await create_company()

        self.agent: Agent = await create_agent(
            self.company, email=self.__agent_email, password=self.__agent_password
        )

    async def test_create(self) -> None:
        async with database.create_async_session() as session:
            repository: ICreateRepository[IAgentCreateRepository, Optional[Agent]] = (
                AgentRepository(session)
            )

            repository_params: IAgentCreateRepository = Mock(
                email="usuario_teste@gmail.com",
                password="1234",
                company=self.company,
            )

            repository_params.name = "Usuário Teste"

            agent: Optional[Agent] = await repository.create(repository_params)

            await session.commit()

            self.assertIsNotNone(agent)

    async def test_update(self) -> None:
        async with database.create_async_session() as session:
            repository: IUpdateRepository[IAgentUpdateRepository, Optional[Agent]] = (
                AgentRepository(session)
            )

            repository_params: IAgentUpdateRepository = Mock(
                email="usuario_teste_alterado@gmail.com",
                password="1234",
                uuid=self.agent.uuid,
                company=self.company,
                instance=None,
            )

            repository_params.name = "Usuário Teste"

            agent: Optional[Agent] = await repository.update(repository_params)

            await session.commit()

            self.assertIsNotNone(agent)

    async def test_delete(self) -> None:
        async with database.create_async_session() as session:
            repository: IDeleteRepository[IAgentDeleteRepository, Optional[Agent]] = (
                AgentRepository(session)
            )

            repository_params: IAgentDeleteRepository = Mock(
                uuid=self.agent.uuid,
                instance=None,
            )

            agent: Optional[Agent] = await repository.delete(repository_params)

            await session.commit()

            self.assertIsNotNone(agent)

    async def test_find(self) -> None:
        async with database.create_async_session() as session:
            repository: IFindRepository[IAgentFindRepository, Optional[Agent]] = (
                AgentRepository(session)
            )

            repository_params: IAgentFindRepository = Mock(uuid=self.agent.uuid)

            agent: Optional[Agent] = await repository.find(repository_params)

            self.assertIsNotNone(agent)

    async def test_find_many(self) -> None:
        limit: int = 10

        page: int = 0

        async with database.create_async_session() as session:
            repository: IFindManyRepository[
                IAgentFindManyRepository, Optional[Agent]
            ] = AgentRepository(session)

            repository_params: IAgentFindManyRepository = Mock(
                company=self.company, limit=limit, page=page
            )

            agents: Sequence[Agent] = await repository.find_many(repository_params)

            self.assertTrue(len(agents) > 0)

            self.assertTrue(len(agents) <= limit)

            self.assertTrue(agents)

    async def test_auth(self) -> None:
        async with database.create_async_session() as session:
            repository: IAuthRepository[IAgentAuthRepository, Optional[Agent]] = (
                AgentRepository(session)
            )

            repository_params: IAgentAuthRepository = Mock(
                email=self.__agent_email, password=self.__agent_password
            )

            agent: Agent = await repository.auth(repository_params)

            logging.info(f"Agent Auth: {agent}\n")

            self.assertIsNotNone(agent)
