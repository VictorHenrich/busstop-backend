from typing import Any, Tuple, Type, List, Union
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.session import sessionmaker, Session
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
import logging

from utils.types import DictType, DatabaseDialectType


class ServerDatabase:
    _mapped_dialects = {
        DatabaseDialectType.POSTGRESQL: {
            "name": "postgresql",
            "default_lib": "psycopg2",
            "async_lib": "asyncpg",
        },
        DatabaseDialectType.MYSQL: {
            "name": "mysql",
            "default_lib": "PyMySQL",
            "async_lib": "aiomysql",
        },
        DatabaseDialectType.SQLITE: {
            "name": "sqlite",
            "default_lib": None,
            "async_lib": "aiosqlite",
        },
    }

    def __create_url(
        self,
        host: str,
        port: Union[str, int],
        dbname: str,
        username: str,
        password: str,
        in_memory: bool,
        dialect: DatabaseDialectType,
    ) -> Tuple[str, str]:
        dialect_data: DictType[str, str] = ServerDatabase._mapped_dialects[dialect]

        url: str = (
            ":///:memory:"
            if in_memory is True
            else f"://{username}:{password}@{host}:{port}/{dbname}"
        )

        url_default: str = f"{dialect_data['name']}"

        url_async: str = f"{dialect_data['name']}"

        if not dialect_data["default_lib"]:
            url_default += url

        if not dialect_data["async_lib"]:
            url_async += url

        if dialect_data["default_lib"] is not None:
            url_default += f"+{dialect_data['default_lib']}{url}"

        if dialect_data["async_lib"] is not None:
            url_async += f"+{dialect_data['async_lib']}{url}"

        return url_default, url_async

    def __create_base(self) -> Type[DeclarativeBase]:
        class Base(DeclarativeBase):
            pass

        return Base

    def __init__(
        self,
        host: str,
        port: Union[str, int],
        dbname: str,
        username: str,
        password: str,
        dialect: DatabaseDialectType,
        in_memory: bool = False,
        instance_name: str = "main",
    ) -> None:
        self.__url, self.__async_url = self.__create_url(
            host, port, dbname, username, password, in_memory, dialect
        )

        self.__engine: Engine = create_engine(self.__url)

        self.__async_engine: AsyncEngine = create_async_engine(self.__async_url)

        self.__Base: Type[DeclarativeBase] = self.__create_base()

        self.__instance_name: str = instance_name

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def async_engine(self) -> AsyncEngine:
        return self.__async_engine

    @property
    def Base(self) -> Type[DeclarativeBase]:
        return self.__Base

    @property
    def instance_name(self) -> str:
        return self.__instance_name

    @property
    def url(self) -> str:
        return self.__url

    @property
    def async_url(self) -> str:
        return self.__async_url

    @Base.setter
    def Base(self, base_cls: Type[DeclarativeBase]) -> None:
        self.__Base = base_cls

    def create_session(self, **kwargs: Any) -> Session:
        return sessionmaker(self.__engine, class_=Session, **kwargs)()

    def create_async_session(self, **kwargs: Any) -> AsyncSession:
        return async_sessionmaker(self.__async_engine, **kwargs)()

    def create_all(self) -> None:
        self.__Base.metadata.create_all(self.__engine)

    def drop_all(self) -> None:
        self.__Base.metadata.drop_all(self.__engine)

    async def create_all_async(self) -> None:
        async with self.__async_engine.begin() as conn:
            logging.warning(f"Creating all database tables")

            await conn.run_sync(self.__Base.metadata.create_all)

    async def drop_all_async(self) -> None:
        async with self.__async_engine.begin() as conn:
            logging.warning(f"Deleting all database tables")

            await conn.run_sync(self.__Base.metadata.drop_all)


class ServerDatabases:
    def __init__(self, *bases: ServerDatabase) -> None:
        self.__bases: List[ServerDatabase] = list(bases)

    def insert_database(self, database: ServerDatabase) -> None:
        self.__bases.append(database)

    def remove_database(self, database: ServerDatabase) -> None:
        self.__bases.remove(database)

    def set_databases(self, *databases: ServerDatabase):
        self.__bases = list(databases)

    def select(self, instance_name: str = "main") -> ServerDatabase:
        for base in self.__bases:
            if instance_name == base.instance_name:
                return base

        raise Exception(f"The name of the '{instance_name}' database was not found")
