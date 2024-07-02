from typing import Optional, Protocol, Mapping, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update, update, Delete, delete, Select, select, func

from models import User
from utils.patterns import (
    BaseRepository,
    ICreateRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindRepository,
    IAuthRepository,
)
from utils.exceptions import UserNotFound, InvalidUserPassword
from utils.crypt import CryptUtils
from utils.functions import handle_dict


class UserCreationRepositoryProps(Protocol):
    name: str
    email: str
    password: str


class UserUpdateRepositoryProps(Protocol):
    name: str
    email: str
    password: str
    uuid: str
    instance: Optional[User]


class UserCaptureRepositoryProps(Protocol):
    uuid: str


class UserExclusionRepositoryProps(Protocol):
    uuid: str
    instance: Optional[User]


class UserAuthRepositoryProps(Protocol):
    email: str
    password: str


class UserRepository(
    BaseRepository[AsyncSession],
    ICreateRepository[UserCreationRepositoryProps, User],
    IUpdateRepository[UserUpdateRepositoryProps, Optional[User]],
    IDeleteRepository[UserExclusionRepositoryProps, Optional[User]],
    IFindRepository[UserCaptureRepositoryProps, User],
    IAuthRepository[UserAuthRepositoryProps, User],
):
    async def create(self, props: UserCreationRepositoryProps) -> User:
        user: User = User(
            name=props.name,
            email=props.email,
            password=CryptUtils.Bcrypt.create_hash(props.password),
        )

        self.session.add(user)

        return user

    async def update(self, props: UserUpdateRepositoryProps) -> Optional[User]:
        password: Optional[str] = None

        if props.password:
            password = CryptUtils.Bcrypt.create_hash(props.password)

        if props.instance:
            props.instance.name = props.name
            props.instance.email = props.email

            if password:
                props.instance.password = password

            self.session.add(props.instance)

            return props.instance

        else:
            data: Mapping[str, Any] = {
                "name": props.name,
                "email": props.email,
                "password": password,
            }

            query: Update = (
                update(User).values(**handle_dict(data)).where(User.uuid == props.uuid)
            )

            return await self.session.scalar(query)

    async def delete(self, props: UserExclusionRepositoryProps) -> Optional[User]:
        if props.instance:
            await self.session.delete(props.instance)

            return props.instance

        else:
            query: Delete = delete(User).where(User.uuid == props.uuid)

            return await self.session.scalar(query)

    async def find(self, props: UserCaptureRepositoryProps) -> Optional[User]:
        query: Select = select(User).where(User.uuid == props.uuid)

        return await self.session.scalar(query)

    async def auth(self, props: UserAuthRepositoryProps) -> User:
        query: Select = select(User).where(func.lower(User.email) == props.email)

        user: Optional[User] = await self.session.scalar(query)

        if not user:
            raise UserNotFound(props.email)

        if not CryptUtils.Bcrypt.compare_password(props.password, user.password):
            raise InvalidUserPassword(user)

        return user
