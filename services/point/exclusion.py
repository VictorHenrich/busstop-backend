from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from server.instances import ServerInstances
from server.database import Database
from models import Point
from repositories.point import PointRepository, PointExclusionRepositoryProps
from utils.patterns import IService, IDeleteRepository, AbstractBaseEntity
from utils.constants import DATABASE_INSTANCE_NAME


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

        await session.commit()

        return point

    async def execute(self) -> Optional[Point]:
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            return await self.__delete_point(session)
