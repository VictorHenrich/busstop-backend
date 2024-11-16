from typing import Optional, Protocol, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update, update, delete, Select, select, func
from sqlalchemy.orm import joinedload

from models import Company, Agent
from utils.patterns import (
    BaseRepository,
    ICreateRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindRepository,
    IFindManyRepository,
    IAuthRepository,
)
from utils.exceptions import UserNotFound, InvalidUserPassword
from utils.crypt import CryptUtils
from utils.types import DictType


class IAgentCreateRepository(Protocol):
    name: str

    email: str

    password: str

    company: Company


class IAgentUpdateRepository(Protocol):
    uuid: str

    name: str

    email: str

    password: str

    instance: Optional[Agent]


class IAgentDeleteRepository(Protocol):
    uuid: str
    instance: Optional[Agent]


class IAgentFindRepository(Protocol):
    uuid: str


class IAgentFindManyRepository(Protocol):
    company: Company
    page: int
    limit: int


class IAgentAuthRepository(Protocol):
    email: str

    password: str


class AgentRepository(
    BaseRepository[AsyncSession],
    ICreateRepository[IAgentCreateRepository, Optional[Agent]],
    IUpdateRepository[IAgentUpdateRepository, Optional[Agent]],
    IDeleteRepository[IAgentDeleteRepository, Optional[Agent]],
    IFindRepository[IAgentFindRepository, Agent],
    IFindManyRepository[IAgentFindManyRepository, Agent],
    IAuthRepository[IAgentAuthRepository, Agent],
):
    async def create(self, props: IAgentCreateRepository) -> Optional[Agent]:
        agent: Agent = Agent()

        agent.company = props.company
        agent.name = props.name
        agent.email = props.email
        agent.password = CryptUtils.Bcrypt.create_hash(props.password)

        self.session.add(agent)

        return agent

    async def update(self, props: IAgentUpdateRepository) -> Optional[Agent]:
        password: Optional[str] = props.password

        if password is not None:
            password = CryptUtils.Bcrypt.create_hash(password)

        if props.instance:
            props.instance.name = props.name
            props.instance.email = props.email

            if password is not None:
                props.instance.password = password

            self.session.add(props.instance)

            return props.instance

        else:
            data: DictType = {
                "name": props.name,
                "email": props.email,
                "password": password,
            }

            data = {name: value for name, value in data.items() if value is not None}

            query: Update = (
                update(Agent)
                .where(Agent.uuid == props.uuid)
                .values(**data)
                .returning(Agent)
            )

            return await self.session.scalar(query)

    async def delete(self, props: IAgentDeleteRepository) -> Optional[Agent]:
        if props.instance:
            await self.session.delete(props.instance)

            return props.instance

        else:
            query = delete(Agent).where(Agent.uuid == props.uuid)

            return await self.session.scalar(query.returning(Agent))

    async def find(self, props: IAgentFindRepository) -> Optional[Agent]:
        query: Select = (
            select(Agent)
            .where(Agent.uuid == props.uuid)
            .options(joinedload(Agent.company))
        )

        return await self.session.scalar(query)

    async def find_many(self, props: IAgentFindManyRepository) -> Sequence[Agent]:
        query: Select = (
            select(Agent)
            .join(Company, Agent.company_id == Company.id)
            .options(joinedload(Agent.company))
            .where(Agent.company_id == props.company.id)
            .offset(props.page)
            .limit(props.limit)
        )

        return (await self.session.scalars(query)).all()

    async def auth(self, props: IAgentAuthRepository) -> Agent:
        query: Select = (
            select(Agent)
            .options(joinedload(Agent.company))
            .where(func.lower(Agent.email) == props.email)
        )

        agent: Optional[Agent] = await self.session.scalar(query)

        if agent is None:
            raise UserNotFound(props.email)

        if not CryptUtils.Bcrypt.compare_password(props.password, agent.password):
            raise InvalidUserPassword(agent)

        return agent
