from typing import (
    Generic,
    Optional,
    TypeVar,
    Awaitable,
    Union,
    Protocol,
    Union,
    Sequence,
)
from abc import ABC
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession


SPT = TypeVar("SPT", bound=BaseModel, covariant=True)

SRT = TypeVar("SRT", covariant=True)

RPT = TypeVar("RPT", contravariant=True)

RRT = TypeVar("RRT", covariant=True)

BST = TypeVar("BST", bound=Union[Session, AsyncSession])


class BaseRepository(ABC, Generic[BST]):
    def __init__(self, session: BST) -> None:
        self.__session: BST = session

    @property
    def session(self) -> BST:
        return self.__session


class ICreateRepository(Protocol, Generic[RPT, RRT]):
    def create(self, props: RPT) -> Union[Awaitable[RRT], RRT]:
        ...


class IUpdateRepository(Protocol, Generic[RPT, RRT]):
    def update(self, props: RPT) -> Union[Awaitable[RRT], RRT]:
        ...


class IDeleteRepository(Protocol, Generic[RPT, RRT]):
    def delete(self, props: RPT) -> Union[Awaitable[RRT], RRT]:
        ...


class IFindRepository(Protocol, Generic[RPT, RRT]):
    def find(self, props: RPT) -> Union[Awaitable[Optional[RRT]], Optional[RRT]]:
        ...


class ICreateManyRepository(Protocol, Generic[RPT, RRT]):
    def create_many(self, props: RPT) -> Union[Awaitable[RRT], RRT]:
        ...


class IUpdateManyRepository(Protocol, Generic[RPT, RRT]):
    def update_many(self, props: RPT) -> Union[Awaitable[RRT], RRT]:
        ...


class IDeleteManyRepository(Protocol, Generic[RPT, RRT]):
    def delete_many(self, props: RPT) -> Union[Awaitable[RRT], RRT]:
        ...


class IFindManyRepository(Protocol, Generic[RPT, RRT]):
    def find_many(self, props: RPT) -> Union[Awaitable[Sequence[RRT]], Sequence[RRT]]:
        ...


class IAuthRepository(Protocol, Generic[RPT, RRT]):
    def auth(self, props: RPT) -> Union[Awaitable[RRT], RRT]:
        ...


class AbstractBaseEntity(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)
