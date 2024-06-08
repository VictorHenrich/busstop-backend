from models import database, Agent
from repositories.agent import AgentRepository, AgentAuthRepositoryProps 
from utils.patterns import AbstractBaseEntity



class AgentAuthProps(AbstractBaseEntity):
    email: str

    password: str


class AuthService:
    async def auth_agent(self, email: str, password: str) -> Agent:
        async with database.create_async_session() as session:
            agent_repository: AgentRepository = AgentRepository(session)

            agent_props: AgentAuthRepositoryProps = AgentAuthProps(
                email=email, password=password
            )

            return await agent_repository.auth(agent_props)