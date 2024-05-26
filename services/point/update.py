from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from server.instances import ServerInstances
from server.database import Database
from models import Point
from repositories.point import PointRepository, PointUpdateRepositoryProps
from utils.patterns import IService, IUpdateRepository, AbstractBaseEntity
from utils.constants import DATABASE_INSTANCE_NAME


class PointUpdateProps(AbstractBaseEntity):
    uuid: str

    address_state: Optional[str]

    address_city: Optional[str]

    address_neighborhood: Optional[str]

    address_street: Optional[str]

    address_number: Optional[str]

    latitude: Optional[str]

    longitude: Optional[str]

    point_instance: Optional[Point] = None


class PointUpdateService(IService[Optional[Point]]):
    def __init__(
        self,
        point_uuid: str,
        address_state: Optional[str],
        address_city: Optional[str],
        address_neighborhood: Optional[str],
        address_street: Optional[str],
        address_number: Optional[str],
        latitude: Optional[str],
        longitude: Optional[str],
    ) -> None:
        self.__point_uuid: str = point_uuid

        self.__address_state: Optional[str] = address_state

        self.__address_city: Optional[str] = address_city

        self.__address_neighborhood: Optional[str] = address_neighborhood

        self.__address_street: Optional[str] = address_street

        self.__address_number: Optional[str] = address_number

        self.__latitude: Optional[str] = latitude

        self.__longitude: Optional[str] = longitude

    async def __update_point(self, session: AsyncSession) -> Optional[Point]:
        data: PointUpdateProps = PointUpdateProps(
            address_state=self.__address_state,
            address_city=self.__address_city,
            address_neighborhood=self.__address_neighborhood,
            address_street=self.__address_street,
            address_number=self.__address_number,
            latitude=self.__latitude,
            longitude=self.__longitude,
            uuid=self.__point_uuid,
        )

        company_repository: IUpdateRepository[
            PointUpdateRepositoryProps, Optional[Point]
        ] = PointRepository(session)

        point: Optional[Point] = await company_repository.update(data)

        await session.commit()

        await session.refresh(point)

        return point

    async def execute(self) -> Optional[Point]:
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            return await self.__update_point(session)
