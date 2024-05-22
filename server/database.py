from typing import Any, Mapping, Tuple, Type, List, Union
from enum import Enum
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.session import sessionmaker, Session
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)


class DatabaseDialects(Enum):
    POSTGRESQL = {"name": "postgresql", "default": "psycopg2", "async": "asyncpg"}

    MYSQL = {"name": "mysql", "default": "PyMySQL", "async": "aiomysql"}


class Database:
    def __create_url(
        self,
        host: str,
        port: Union[str, int],
        dbname: str,
        username: str,
        password: str,
        dialect: DatabaseDialects,
    ) -> Tuple[str, str]:
        dialect_data: Mapping[str, str] = dialect.value

        url: str = f"://{username}:{password}@{host}:{port}/{dbname}"

        url_default: str = f"{dialect_data['name']}+{dialect_data['default']}{url}"

        url_async: str = f"{dialect_data['name']}+{dialect_data['async']}{url}"

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
        dialect: DatabaseDialects,
        instance_name: str = "main",
    ) -> None:
        url, url_async = self.__create_url(
            host, port, dbname, username, password, dialect
        )

        self.__engine: Engine = create_engine(url)

        self.__async_engine: AsyncEngine = create_async_engine(url_async)

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
            await conn.run_sync(self.__Base.metadata.create_all)

    async def drop_all_async(self) -> None:
        async with self.__async_engine.begin() as conn:
            await conn.run_sync(self.__Base.metadata.drop_all)


class Databases:
    def __init__(self, *bases: Database) -> None:
        self.__bases: List[Database] = list(bases)

    def insert_database(self, database: Database) -> None:
        self.__bases.append(database)

    def select(self, instance_name: str = "main") -> Database:
        for base in self.__bases:
            if instance_name == base.instance_name:
                return base

        raise Exception(f"The name of the '{instance_name}' database was not found")
