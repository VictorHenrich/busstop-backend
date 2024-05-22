from typing import Generic, Any, TypeVar, Awaitable, Union, Protocol, Union
from abc import ABC
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession


ST = TypeVar("ST", bound=Union[Awaitable[Any], Any], covariant=True)

RTP = TypeVar("RTP", bound=Any, contravariant=True)

RTR = TypeVar("RTR", bound=Union[Any, None], covariant=True)

BRT = TypeVar("BRT", bound=Union[Session, AsyncSession])


class IService(Protocol, Generic[ST]):
    def execute(self) -> ST:
        ...


class BaseRepository(ABC, Generic[BRT]):
    def __init__(self, session: BRT) -> None:
        self.__session: BRT = session

    @property
    def session(self) -> BRT:
        return self.__session


class CreateRepository(Protocol, Generic[RTP, RTR]):
    def create(self, params: RTP) -> RTR:
        ...


class UpdateRepository(Protocol, Generic[RTP, RTR]):
    def update(self, params: RTP) -> RTR:
        ...


class DeleteRepository(Protocol, Generic[RTP, RTR]):
    def delete(self, params: RTP) -> RTR:
        ...


class GetRepository(Protocol, Generic[RTP, RTR]):
    def get(self, params: RTP) -> RTR:
        ...


class CreateManyRepository(Protocol, Generic[RTP, RTR]):
    def create_many(self, params: RTP) -> RTR:
        ...


class UpdateManyRepository(Protocol, Generic[RTP, RTR]):
    def update_many(self, params: RTP) -> RTR:
        ...


class DeleteManyRepository(Protocol, Generic[RTP, RTR]):
    def delete_many(self, params: RTP) -> RTR:
        ...


class GetManyRepository(Protocol, Generic[RTP, RTR]):
    def get_many(self, params: RTP) -> RTR:
        ...
