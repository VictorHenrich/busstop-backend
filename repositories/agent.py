from typing import Optional, Protocol, Sequence, Mapping, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update, update, Delete, delete, Select, select, func
from sqlalchemy.orm import joinedload
from copy import copy

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


class AgentCreationRepositoryProps(Protocol):
    name: str

    email: str

    password: str

    company: Company


class AgentUpdateRepositoryProps(Protocol):
    uuid: str

    name: str

    email: str

    password: str

    instance: Optional[Agent]


class AgentExclusionRepositoryProps(Protocol):
    uuid: str
    instance: Optional[Agent] = None


class AgentCaptureRepositoryProps(Protocol):
    uuid: str


class AgentListingRepositoryProps(Protocol):
    company: Company


class AgentAuthRepositoryProps(Protocol):
    email: str

    password: str


class AgentRepository(
    BaseRepository[AsyncSession],
    ICreateRepository[AgentCreationRepositoryProps, Optional[Agent]],
    IUpdateRepository[AgentUpdateRepositoryProps, Optional[Agent]],
    IDeleteRepository[AgentExclusionRepositoryProps, Optional[Agent]],
    IFindRepository[AgentCaptureRepositoryProps, Agent],
    IFindManyRepository[AgentListingRepositoryProps, Agent],
    IAuthRepository[AgentAuthRepositoryProps, Agent],
):
    async def create(self, props: AgentCreationRepositoryProps) -> Optional[Agent]:
        agent: Agent = Agent()

        agent.company = props.company
        agent.name = props.name
        agent.email = props.email
        agent.password = CryptUtils.Bcrypt.create_hash(props.password)

        self.session.add(agent)

        return agent

    async def update(self, props: AgentUpdateRepositoryProps) -> Optional[Agent]:
        password: Optional[str] = props.password

        if password is not None:
            password = CryptUtils.Bcrypt.create_hash(password)

        data: Mapping[str, Any] = {
            "name": props.name,
            "email": props.email,
            "password": password,
        }

        data = {name: value for name, value in data.items() if value is not None}

        if props.instance:
            props.instance.name = props.name
            props.instance.email = props.email

            if password is not None:
                props.instance.password = password

            self.session.add(props.instance)

            return props.instance

        else:
            query: Update = (
                update(Agent)
                .where(Agent.uuid == props.uuid)
                .values(**data)
                .returning(Agent)
            )

            return await self.session.scalar(query)

    async def delete(self, props: AgentExclusionRepositoryProps) -> Optional[Agent]:
        agent: Optional[Agent] = None

        if props.instance:
            await self.session.delete(props.instance)

            agent = props.instance

        else:
            query: Delete = delete(Agent).where(Agent.uuid == props.uuid)

            agent = await self.session.scalar(query)

        if agent is not None:
            copy(agent)

    async def find(self, props: AgentCaptureRepositoryProps) -> Optional[Agent]:
        query: Select = (
            select(Agent)
            .where(Agent.uuid == props.uuid)
            .options(joinedload(Agent.company))
        )

        return await self.session.scalar(query)

    async def find_many(self, props: AgentListingRepositoryProps) -> Sequence[Agent]:
        query: Select = (
            select(Agent)
            .join(Company, Agent.company_id == Company.id)
            .options(joinedload(Agent.company))
            .where(Agent.company_id == props.company.id)
        )

        return (await self.session.scalars(query)).all()

    async def auth(self, props: AgentAuthRepositoryProps) -> Agent:
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
