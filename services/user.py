from typing import Optional
from copy import copy

from models import database, User
from repositories.user import (
    UserRepository,
    IUserCreateRepository,
    IUserUpdateRepository,
    IUserDeleteRepository,
    IUserFindRepository,
)
from utils.patterns import (
    ICreateRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindRepository,
    AbstractBaseEntity,
)
from utils.exceptions import ModelNotFound


class UserCreationProps(AbstractBaseEntity):
    name: str
    email: str
    password: str


class UserUpdateProps(AbstractBaseEntity):
    name: str
    email: str
    password: str
    uuid: str
    instance: Optional[User] = None


class UserExclusionProps(AbstractBaseEntity):
    uuid: str
    instance: Optional[User] = None


class UserCaptureProps(AbstractBaseEntity):
    uuid: str


class UserService:
    async def create_user(self, name: str, email: str, password: str) -> User:
        async with database.create_async_session() as session:
            user_repository: ICreateRepository[
                IUserCreateRepository, User
            ] = UserRepository(session)

            user_creation_props: IUserCreateRepository = UserCreationProps(
                name=name, email=email, password=password
            )

            user: User = await user_repository.create(user_creation_props)

            await session.commit()

            await session.refresh(user)

            return user

    async def update_user(
        self, name: str, email: str, password: str, user_uuid: str
    ) -> User:
        async with database.create_async_session() as session:
            user_repository: IUpdateRepository[
                IUserUpdateRepository, Optional[User]
            ] = UserRepository(session)

            user_update_props: IUserUpdateRepository = UserUpdateProps(
                name=name, email=email, password=password, uuid=user_uuid
            )

            user: Optional[User] = await user_repository.update(user_update_props)

            await session.commit()

            if user is None:
                raise ModelNotFound(User, user_uuid)

            await session.refresh(user)

            return user

    async def delete_user(self, user_uuid: str) -> User:
        async with database.create_async_session() as session:
            user_repository: IDeleteRepository[
                IUserDeleteRepository, Optional[User]
            ] = UserRepository(session)

            user_exclusion_props: IUserDeleteRepository = UserExclusionProps(
                uuid=user_uuid
            )

            user: Optional[User] = await user_repository.delete(user_exclusion_props)

            if user is None:
                raise ModelNotFound(User, user_uuid)

            return copy(user)

    async def find_user(self, user_uuid: str) -> User:
        async with database.create_async_session() as session:
            user_repository: IFindRepository[
                IUserFindRepository, Optional[User]
            ] = UserRepository(session)

            user_capture_props: IUserFindRepository = UserCaptureProps(uuid=user_uuid)

            user: Optional[User] = await user_repository.find(user_capture_props)

            if user is None:
                raise ModelNotFound(User, user_uuid)

            return user
