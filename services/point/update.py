from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from models import Point, database
from repositories.point import PointRepository, PointUpdateRepositoryProps
from utils.patterns import IService, IUpdateRepository, AbstractBaseEntity


class PointUpdateProps(AbstractBaseEntity):
    uuid: str

    address_state: str

    address_city: str

    address_neighborhood: str

    address_street: str

    address_number: str

    latitude: str

    longitude: str

    point_instance: Optional[Point] = None


class PointUpdateService(IService[Optional[Point]]):
    def __init__(
        self,
        point_uuid: str,
        address_state: str,
        address_city: str,
        address_neighborhood: str,
        address_street: str,
        address_number: str,
        latitude: str,
        longitude: str,
    ) -> None:
        self.__point_uuid: str = point_uuid

        self.__address_state: str = address_state

        self.__address_city: str = address_city

        self.__address_neighborhood: str = address_neighborhood

        self.__address_street: str = address_street

        self.__address_number: str = address_number

        self.__latitude: str = latitude

        self.__longitude: str = longitude

    async def __update_point(self, session: AsyncSession) -> Optional[Point]:
        data: PointUpdateRepositoryProps = PointUpdateProps(
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
        async with database.create_async_session() as session:
            return await self.__update_point(session)
