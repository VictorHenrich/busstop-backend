from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from copy import copy

from models import Point, database
from repositories.point import PointRepository, PointExclusionRepositoryProps
from utils.patterns import IService, IDeleteRepository, AbstractBaseEntity


class PointExclusionProps(AbstractBaseEntity):
    uuid: str


class PointExclusionService(IService[Optional[Point]]):
    def __init__(self, point_uuid: str) -> None:
        self.__point_uuid: str = point_uuid

    async def __delete_point(self, session: AsyncSession) -> Optional[Point]:
        data: PointExclusionProps = PointExclusionProps(uuid=self.__point_uuid)

        company_repository: IDeleteRepository[
            PointExclusionRepositoryProps, Optional[Point]
        ] = PointRepository(session)

        point: Optional[Point] = await company_repository.delete(data)

        point_copy: Optional[Point] = None

        if point:
            point_copy = copy(point)

        await session.commit()

        return point_copy

    async def execute(self) -> Optional[Point]:
        async with database.create_async_session() as session:
            return await self.__delete_point(session)
