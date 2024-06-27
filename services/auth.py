from typing import Mapping, Literal

from models import database, Agent
from repositories.agent import AgentRepository, AgentAuthRepositoryProps
from services.agent import AgentService
from utils.entities import TokenDataEntity
from utils.patterns import AbstractBaseEntity, IAuthRepository
from utils.crypt import CryptUtils
from utils.constants import TOKEN_EXPIRATION_MINUTE, REFRESH_TOKEN_EXPIRATION_MINUTE
from utils.exceptions import InvalidToken


class AgentAuthProps(AbstractBaseEntity):
    email: str

    password: str


class AuthService:
    def __init__(self) -> None:
        self.__agent_service: AgentService = AgentService()

    def __create_token(self, agent: Agent) -> str:
        return CryptUtils.Jwt.create_token(
            agent_uuid=agent.uuid,
            company_uuid=agent.company.uuid,
            expiration_minute=TOKEN_EXPIRATION_MINUTE,
            is_refresh=False,
        )

    def __create_refresh_token(self, agent: Agent) -> str:
        return CryptUtils.Jwt.create_token(
            agent_uuid=agent.uuid,
            company_uuid=agent.company.uuid,
            expiration_minute=REFRESH_TOKEN_EXPIRATION_MINUTE,
            is_refresh=True,
        )

    async def auth_agent(
        self, email: str, password: str
    ) -> Mapping[Literal["token", "refresh_token"], str]:
        async with database.create_async_session() as session:
            agent_repository: IAuthRepository[
                AgentAuthRepositoryProps, Agent
            ] = AgentRepository(session)

            agent_props: AgentAuthRepositoryProps = AgentAuthProps(
                email=email, password=password
            )

            agent: Agent = await agent_repository.auth(agent_props)

            token: str = self.__create_token(agent)

            refresh_token: str = self.__create_refresh_token(agent)

            return {"token": token, "refresh_token": refresh_token}

    async def get_user_data_in_token(self, token: str) -> Agent:
        token_handled: str = token.replace("Bearer", "").strip()

        token_data: TokenDataEntity = CryptUtils.Jwt.decode_token(token_handled)

        return await self.__agent_service.find_agent(token_data.agent_uuid)

    async def refresh_token(self, token: str) -> str:
        token_data: TokenDataEntity = CryptUtils.Jwt.decode_token(token)

        if not token_data.is_refresh:
            raise InvalidToken(token)

        agent: Agent = await self.__agent_service.find_agent(token_data.agent_uuid)

        return self.__create_token(agent)
