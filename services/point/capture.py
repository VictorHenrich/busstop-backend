from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from models import Point, database
from repositories.point import PointRepository, PointCaptureRepositoryProps
from utils.patterns import IService, IFindRepository, AbstractBaseEntity


class PointCaptureProps(AbstractBaseEntity):
    uuid: str


class PointCaptureService(IService[Optional[Point]]):
    def __init__(self, point_uuid: str) -> None:
        self.__point_uuid: str = point_uuid

    async def __find_point(self, session: AsyncSession) -> Optional[Point]:
        data: PointCaptureProps = PointCaptureProps(uuid=self.__point_uuid)

        company_repository: IFindRepository[
            PointCaptureRepositoryProps, Optional[Point]
        ] = PointRepository(session)

        return await company_repository.find(data)

    async def execute(self) -> Optional[Point]:
        async with database.create_async_session() as session:
            return await self.__find_point(session)
