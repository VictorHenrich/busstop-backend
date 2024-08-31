from typing import Optional, Sequence
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, patch
import logging

from models import Agent, database
from repositories.agent import (
    AgentRepository,
    IAgentCreateRepository,
    IAgentUpdateRepository,
    IAgentDeleteRepository,
    IAgentFindRepository,
    IAgentFindManyRepository,
    IAgentAuthRepository,
)
from utils.patterns import (
    IAuthRepository,
    ICreateRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindRepository,
    IFindManyRepository,
)
from utils.crypt import CryptUtils
from .common import AsyncBaseRepositoryOnlineTestCase


class AgentRepositoryOfflineTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_company: Mock = Mock(
            company_name="Empresa Teste",
            fantasy_name="Nome Fantasia TESTE",
            document_cnpj="00000000",
            email="teste@gmail.com",
            uuid="6df97b7d-2beb-4d60-ae75-b742ac3df68a",
        )

        self.__mock_agent: Mock = Mock(
            name="Victor Henrich",
            email="victorhenrich993@gmail.com",
            password="$2a$12$jDnTa113wnAmvD31BiIWwOPfigr2KbFK1M.wW5ACbik1xIVOhXKFm",
            uuid="6df97b7d-2beb-4d60-ae75-b742ac3dak8a",
            company=self.__mock_company,
        )

        self.__mock_async_session: AsyncMock = AsyncMock()

        self.__mock_session: Mock = Mock()

        self.__mock_async_session.scalar.return_value = self.__mock_agent

        mock_all_function: Mock = Mock()

        mock_all_function.all.return_value = [self.__mock_agent]

        self.__mock_async_session.scalars.return_value = mock_all_function

        self.__mock_session.add.return_value = None

    @patch("repositories.agent.Agent", spec=Agent)
    @patch.object(CryptUtils.Bcrypt, "create_hash")
    async def test_create_agent(
        self, mock_create_hash_function: Mock, mock_agent_model_class: Mock
    ) -> None:
        mock_create_hash_function.return_value = self.__mock_agent.password

        mock_agent_model_class.return_value = self.__mock_agent

        agent_repository: ICreateRepository[IAgentCreateRepository, Optional[Agent]] = (
            AgentRepository(self.__mock_session)
        )

        agent: Optional[Agent] = await agent_repository.create(
            Mock(
                name=self.__mock_agent.name,
                email=self.__mock_agent.email,
                password=self.__mock_agent.password,
                company=self.__mock_company,
            )
        )

        self.__mock_session.add.assert_called_once_with(self.__mock_agent)

        mock_create_hash_function.assert_called_once()

        self.assertEqual(agent, self.__mock_agent)

    @patch.object(CryptUtils.Bcrypt, "create_hash")
    async def test_update_agent(self, mock_create_hash_function: Mock) -> None:
        mock_create_hash_function.return_value = self.__mock_agent.password

        agent_repository: IUpdateRepository[IAgentUpdateRepository, Optional[Agent]] = (
            AgentRepository(self.__mock_async_session)
        )

        agent: Optional[Agent] = await agent_repository.update(
            Mock(
                name=self.__mock_agent.name,
                email=self.__mock_agent.email,
                password=self.__mock_agent.password,
                uuid=self.__mock_agent.uuid,
                instance=None,
            )
        )

        self.__mock_async_session.scalar.assert_awaited_once()

        mock_create_hash_function.assert_called_once()

        self.assertEqual(agent, self.__mock_agent)

    @patch("repositories.agent.copy")
    async def test_delete_agent(self, mock_copy_function: Mock) -> None:
        mock_copy_function.return_value = self.__mock_agent

        agent_repository: IDeleteRepository[IAgentDeleteRepository, Optional[Agent]] = (
            AgentRepository(self.__mock_async_session)
        )

        agent: Optional[Agent] = await agent_repository.delete(
            Mock(uuid=self.__mock_agent.uuid, instance=None)
        )

        self.__mock_async_session.scalar.assert_awaited_once()

        self.assertEqual(agent, self.__mock_agent)

    async def test_find_agent(self) -> None:
        agent_repository: IFindRepository[IAgentFindRepository, Agent] = (
            AgentRepository(self.__mock_async_session)
        )

        agent: Optional[Agent] = await agent_repository.find(
            Mock(uuid=self.__mock_agent.uuid)
        )

        self.__mock_async_session.scalar.assert_awaited_once()

        self.assertEqual(agent, self.__mock_agent)

    async def test_find_agents(self) -> None:
        agent_repository: IFindManyRepository[IAgentFindManyRepository, Agent] = (
            AgentRepository(self.__mock_async_session)
        )

        agents: Sequence[Agent] = await agent_repository.find_many(
            Mock(uuid=self.__mock_agent.uuid, limit=10, page=0)
        )

        self.__mock_async_session.scalars.assert_awaited_once()

        self.assertEqual(agents, [self.__mock_agent])

    @patch.object(CryptUtils.Bcrypt, "compare_password")
    async def test_auth_agent(self, mock_compare_password_function: Mock) -> None:
        mock_compare_password_function.return_value = True

        agent_repository: IAuthRepository[IAgentAuthRepository, Agent] = (
            AgentRepository(self.__mock_async_session)
        )

        agents: Agent = await agent_repository.auth(
            Mock(email=self.__mock_agent.email, password=self.__mock_agent.password)
        )

        self.__mock_async_session.scalar.assert_awaited_once()

        mock_compare_password_function.assert_called_once_with(
            self.__mock_agent.password, self.__mock_agent.password
        )

        self.assertEqual(agents, self.__mock_agent)


class AgentRepositoryOnlineTestCase(AsyncBaseRepositoryOnlineTestCase):
    async def test_create(self) -> None:
        async with database.create_async_session() as session:
            repository: ICreateRepository[IAgentCreateRepository, Optional[Agent]] = (
                AgentRepository(session)
            )

            repository_params: IAgentCreateRepository = Mock(
                email="usuario_teste_novo@gmail.com",
                password="1234",
                company=self.company,
            )

            repository_params.name = "Usuário Teste"

            agent: Optional[Agent] = await repository.create(repository_params)

            logging.info(f"Agent Created: {agent}")

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
            )

            repository_params.name = "Usuário Teste"

            agent: Optional[Agent] = await repository.update(repository_params)

            logging.info(f"Agent Updated: {agent}\n")

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

            logging.info(f"Agent Deleted: {agent}\n")

            await session.commit()

            self.assertIsNotNone(agent)

    async def test_find(self) -> None:
        async with database.create_async_session() as session:
            repository: IFindRepository[IAgentFindRepository, Optional[Agent]] = (
                AgentRepository(session)
            )

            repository_params: IAgentFindRepository = Mock(uuid=self.agent.uuid)

            agent: Optional[Agent] = await repository.find(repository_params)

            logging.info(f"Agent Finded: {agent}\n")

            self.assertIsNotNone(agent)

    async def test_find_many(self) -> None:
        limit: int = 0

        page: int = 0

        async with database.create_async_session() as session:
            repository: IFindManyRepository[
                IAgentFindManyRepository, Optional[Agent]
            ] = AgentRepository(session)

            repository_params: IAgentFindManyRepository = Mock(
                company=self.company, limit=limit, page=page
            )

            agents: Sequence[Agent] = await repository.find_many(repository_params)

            logging.info(f"Agensts Located: {agents}\n")

            self.assertTrue(agents)

    async def test_auth(self) -> None:
        email: str = ""

        password: str = ""

        async with database.create_async_session() as session:
            repository: IAuthRepository[IAgentAuthRepository, Optional[Agent]] = (
                AgentRepository(session)
            )

            repository_params: IAgentCreateRepository = Mock(
                email=email, password=password
            )

            agent: Agent = await repository.auth(repository_params)

            logging.info(f"Agent Auth: {agent}\n")

            self.assertIsNotNone(agent)
