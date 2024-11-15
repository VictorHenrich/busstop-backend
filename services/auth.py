from typing import Literal, TypeAlias

from models import database, Agent, User
from repositories.agent import AgentRepository, IAgentAuthRepository
from repositories.user import UserRepository, IUserAuthRepository
from services.agent import AgentService
from services.user import UserService
from utils.entities import TokenDataEntity, AgentTokenDataEntity
from utils.patterns import AbstractBaseEntity, IAuthRepository
from utils.crypt import CryptUtils
from utils.config import TOKEN_EXPIRATION_MINUTE, REFRESH_TOKEN_EXPIRATION_MINUTE
from utils.exceptions import InvalidToken
from utils.types import DictType


class AgentAuthProps(AbstractBaseEntity):
    email: str

    password: str


class UserAuthProps(AbstractBaseEntity):
    email: str

    password: str


AuthResult: TypeAlias = DictType[Literal["token", "refresh_token"], str]


class AuthService:
    def __init__(self) -> None:
        self.__agent_service: AgentService = AgentService()

        self.__user_service: UserService = UserService()

    def __create_agent_token(self, agent: Agent) -> str:
        return CryptUtils.Jwt.create_token(
            user_uuid=agent.uuid,
            company_uuid=agent.company.uuid,
            expiration_minute=TOKEN_EXPIRATION_MINUTE,
            is_refresh=False,
            entity_class=AgentTokenDataEntity,
        )

    def __create_agent_refresh_token(self, agent: Agent) -> str:
        return CryptUtils.Jwt.create_token(
            user_uuid=agent.uuid,
            company_uuid=agent.company.uuid,
            expiration_minute=REFRESH_TOKEN_EXPIRATION_MINUTE,
            is_refresh=True,
            entity_class=AgentTokenDataEntity,
        )

    def __create_user_token(self, user: User) -> str:
        return CryptUtils.Jwt.create_token(
            user_uuid=user.uuid,
            expiration_minute=TOKEN_EXPIRATION_MINUTE,
            is_refresh=False,
        )

    def __create_user_refresh_token(self, user: User) -> str:
        return CryptUtils.Jwt.create_token(
            user_uuid=user.uuid,
            expiration_minute=REFRESH_TOKEN_EXPIRATION_MINUTE,
            is_refresh=True,
        )

    async def auth_agent(self, email: str, password: str) -> AuthResult:
        async with database.create_async_session() as session:
            agent_repository: IAuthRepository[IAgentAuthRepository, Agent] = (
                AgentRepository(session)
            )

            agent_props: IAgentAuthRepository = AgentAuthProps(
                email=email, password=password
            )

            agent: Agent = await agent_repository.auth(agent_props)

            token: str = self.__create_agent_token(agent)

            refresh_token: str = self.__create_agent_refresh_token(agent)

            return {"token": token, "refresh_token": refresh_token}

    async def get_agent_data_in_token(self, token: str) -> Agent:
        token_handled: str = token.replace("Bearer", "").strip()

        token_data: TokenDataEntity = CryptUtils.Jwt.decode_token(
            token_handled, entity_class=AgentTokenDataEntity
        )

        return await self.__agent_service.find_agent(token_data.user_uuid)

    async def refresh_agent_token(self, token: str) -> str:
        token_data: AgentTokenDataEntity = CryptUtils.Jwt.decode_token(
            token, entity_class=AgentTokenDataEntity
        )

        if not token_data.is_refresh:
            raise InvalidToken(token)

        agent: Agent = await self.__agent_service.find_agent(token_data.user_uuid)

        return self.__create_agent_token(agent)

    async def auth_user(self, email: str, password: str) -> AuthResult:
        async with database.create_async_session() as session:
            user_repository: IAuthRepository[IUserAuthRepository, User] = (
                UserRepository(session)
            )

            user_props: IUserAuthRepository = UserAuthProps(
                email=email, password=password
            )

            user: User = await user_repository.auth(user_props)

            token: str = self.__create_user_token(user)

            refresh_token: str = self.__create_user_refresh_token(user)

            return {"token": token, "refresh_token": refresh_token}

    async def refresh_user_token(self, token: str) -> str:
        token_data: TokenDataEntity = CryptUtils.Jwt.decode_token(token)

        if not token_data.is_refresh:
            raise InvalidToken(token)

        user: User = await self.__user_service.find_user(token_data.user_uuid)

        return self.__create_user_token(user)

    async def get_user_data_in_token(self, token: str) -> User:
        token_handled: str = token.replace("Bearer", "").strip()

        token_data: TokenDataEntity = CryptUtils.Jwt.decode_token(token_handled)

        return await self.__user_service.find_user(token_data.user_uuid)
