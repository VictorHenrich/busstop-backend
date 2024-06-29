from typing import Mapping, Literal
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, patch
import logging


from services.auth import AuthService
from services.agent import AgentService
from models import database, Agent, Company
from repositories.agent import AgentRepository
from utils.crypt import CryptUtils
from utils.exceptions import (
    UserNotFound,
    InvalidUserPassword,
    InvalidToken,
    ModelNotFound,
)


class AuthServiceTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_async_session: AsyncMock = AsyncMock()

        self.__mock_agent_repository: AsyncMock = AsyncMock()

        self.__mock_agent_service: AsyncMock = AsyncMock()

        self.__mock_company: Mock = Mock(
            company_name="Empresa Teste",
            fantasy_name="Nome Fantasia TESTE",
            document_cnpj="00000000",
            email="teste@gmail.com",
            uuid="6df97b7d-2beb-4d60-ae75-b742ac3df68a",
            spec=Company,
        )

        self.__mock_agent: Mock = Mock(
            name="Victor Henrich",
            email="victorhenrich993@gmail.com",
            password="00000000",
            uuid="6df97b7d-2beb-4d60-ae75-b742ac3df111",
            company=self.__mock_company,
            spec=Agent,
        )

        self.__mock_async_session.__aenter__.return_value = self.__mock_async_session

        self.__mock_agent_repository.auth.return_value = self.__mock_agent

        self.__mock_agent_service.find.find_agent = self.__mock_agent

    @patch("services.auth.database", spec=database)
    @patch("services.auth.AgentRepository", spec=AgentRepository)
    async def test_auth_agent(
        self,
        mock_agent_repository_class: Mock,
        mock_database_instance: Mock,
    ) -> None:
        mock_database_instance.create_async_session.return_value = (
            self.__mock_async_session
        )

        mock_agent_repository_class.return_value = self.__mock_agent_repository

        auth_service: AuthService = AuthService()

        token_data: Mapping[
            Literal["token", "refresh_token"], str
        ] = await auth_service.auth_agent(email="", password="")

        logging.info(f"Token Data: {token_data}")

        mock_database_instance.create_async_session.assert_called_once()

        self.__mock_agent_repository.auth.assert_awaited_once()

        self.assertTrue(token_data)

        self.assertEqual(type(token_data["refresh_token"]), str)

        self.assertEqual(type(token_data["token"]), str)

    @patch("services.auth.CryptUtils", spec=CryptUtils)
    @patch("services.auth.database", spec=database)
    @patch("services.auth.AgentRepository", spec=AgentRepository)
    async def test_auth_agent_with_user_none(
        self,
        mock_agent_repository_class: Mock,
        mock_database_instance: Mock,
        mock_crypt_utils_class: Mock,
    ) -> None:
        mock_crypt_utils_class.Jwt.create_token.return_value = ""

        self.__mock_agent_repository.auth.return_value = None

        mock_database_instance.create_async_session.return_value = (
            self.__mock_async_session
        )

        mock_agent_repository_class.return_value = self.__mock_agent_repository

        with self.assertRaises(AttributeError):
            auth_service: AuthService = AuthService()

            await auth_service.auth_agent(
                email=self.__mock_agent.email, password=self.__mock_agent.password
            )

        mock_crypt_utils_class.Jwt.create_token.assert_not_called()

        mock_database_instance.create_async_session.assert_called_once()

        self.__mock_agent_repository.auth.assert_awaited_once()

    @patch("services.auth.database", spec=database)
    @patch("services.auth.AgentRepository", spec=AgentRepository)
    async def test_auth_agent_with_invalid_password(
        self,
        mock_agent_repository_class: Mock,
        mock_database_instance: Mock,
    ) -> None:
        self.__mock_agent_repository.auth.side_effect = InvalidUserPassword(
            self.__mock_agent
        )

        mock_database_instance.create_async_session.return_value = (
            self.__mock_async_session
        )

        mock_agent_repository_class.return_value = self.__mock_agent_repository

        with self.assertRaises(InvalidUserPassword):
            auth_service: AuthService = AuthService()

            await auth_service.auth_agent(
                email=self.__mock_agent.email, password=self.__mock_agent.password
            )

        mock_database_instance.create_async_session.assert_called_once()

        self.__mock_agent_repository.auth.assert_awaited_once()

    @patch("services.auth.database", spec=database)
    @patch("services.auth.AgentRepository", spec=AgentRepository)
    async def test_auth_agent_with_user_not_found(
        self,
        mock_agent_repository_class: Mock,
        mock_database_instance: Mock,
    ) -> None:
        self.__mock_agent_repository.auth.side_effect = UserNotFound("")

        mock_database_instance.create_async_session.return_value = (
            self.__mock_async_session
        )

        mock_agent_repository_class.return_value = self.__mock_agent_repository

        with self.assertRaises(UserNotFound):
            auth_service: AuthService = AuthService()

            await auth_service.auth_agent(
                email=self.__mock_agent.email, password=self.__mock_agent.password
            )

        mock_database_instance.create_async_session.assert_called_once()

        self.__mock_agent_repository.auth.assert_awaited_once()

    @patch("services.auth.CryptUtils", spec=CryptUtils)
    @patch("services.auth.AgentService", spec=AgentService)
    async def test_refresh_token(
        self, mock_agent_service_class: Mock, mock_crypt_utils_class: Mock
    ) -> None:
        token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZ2VudF91dWlkIjoiNmRmOTdiN2QtMmJlYi00ZDYwLWFlNzUtYjc0MmFjM2RmMTExIiwiY29tcGFueV91dWlkIjoiNmRmOTdiN2QtMmJlYi00ZDYwLWFlNzUtYjc0MmFjM2RmNjhhIiwiZXhwIjoxNzE5NjgyODkzLCJpc19yZWZyZXNoIjpmYWxzZX0.uKR-vc7BbOnUZIbcqp2oKnKU5-D7GjKTLCXANmJVOkc"

        mock_crypt_utils_class.Jwt.decode_token.return_value = Mock(
            agent_uuid=self.__mock_agent.uuid,
            company_uuid=self.__mock_company.uuid,
            exp=None,
            is_refresh=True,
        )

        mock_crypt_utils_class.Jwt.create_token.return_value = token

        mock_agent_service_class.return_value = self.__mock_agent_service

        auth_service: AuthService = AuthService()

        refresh_token: str = await auth_service.refresh_token(token="")

        logging.info(f"Refresh Token: {refresh_token}")

        mock_crypt_utils_class.Jwt.create_token.assert_called_once()

        mock_crypt_utils_class.Jwt.decode_token.assert_called_once()

        self.__mock_agent_service.find_agent.assert_awaited_once()

        self.assertEqual(token, refresh_token)

    @patch("services.auth.CryptUtils", spec=CryptUtils)
    @patch("services.auth.AgentService", spec=AgentService)
    async def test_refresh_token_with_invalid_token(
        self, mock_agent_service_class: Mock, mock_crypt_utils_class: Mock
    ) -> None:
        mock_crypt_utils_class.Jwt.decode_token.return_value = Mock(
            is_refresh=False,
        )

        mock_crypt_utils_class.Jwt.create_token.return_value = None

        mock_agent_service_class.return_value = self.__mock_agent_service

        with self.assertRaises(InvalidToken):
            auth_service: AuthService = AuthService()

            await auth_service.refresh_token(token="")

        mock_crypt_utils_class.Jwt.decode_token.assert_called_once()

        mock_crypt_utils_class.Jwt.create_token.assert_not_called()

        self.__mock_agent_service.find_agent.assert_not_awaited()

    @patch("services.auth.CryptUtils", spec=CryptUtils)
    @patch("services.auth.AgentService", spec=AgentService)
    async def test_refresh_token_with_agent_not_found(
        self, mock_agent_service_class: Mock, mock_crypt_utils_class: Mock
    ) -> None:
        mock_crypt_utils_class.Jwt.decode_token.return_value = Mock(
            is_refresh=True,
        )

        self.__mock_agent_service.find_agent.side_effect = ModelNotFound(
            Agent, self.__mock_agent.uuid
        )

        mock_crypt_utils_class.Jwt.create_token.return_value = None

        mock_agent_service_class.return_value = self.__mock_agent_service

        with self.assertRaises(ModelNotFound):
            auth_service: AuthService = AuthService()

            await auth_service.refresh_token(token="")

        self.__mock_agent_service.find_agent.assert_awaited_once()

        mock_crypt_utils_class.Jwt.decode_token.assert_called_once()

        mock_crypt_utils_class.Jwt.create_token.assert_not_called()

    @patch("services.auth.CryptUtils", spec=CryptUtils)
    @patch("services.auth.AgentService", spec=AgentService)
    async def test_refresh_token_with_agent_is_none(
        self, mock_agent_service_class: Mock, mock_crypt_utils_class: Mock
    ) -> None:
        mock_crypt_utils_class.Jwt.decode_token.return_value = Mock(
            is_refresh=True,
        )

        self.__mock_agent_service.find_agent.return_value = None

        mock_crypt_utils_class.Jwt.create_token.return_value = None

        mock_agent_service_class.return_value = self.__mock_agent_service

        with self.assertRaises(AttributeError):
            auth_service: AuthService = AuthService()

            await auth_service.refresh_token(token="")

        self.__mock_agent_service.find_agent.assert_awaited_once()

        mock_crypt_utils_class.Jwt.decode_token.assert_called_once()

        mock_crypt_utils_class.Jwt.create_token.assert_not_called()
