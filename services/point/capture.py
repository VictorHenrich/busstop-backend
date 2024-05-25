from typing import Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from server.instances import ServerInstances
from server.database import Database
from models import Point
from repositories.point import PointRepository, PointCaptureRepositoryProps
from utils.patterns import IService, IFindRepository
from utils.constants import DATABASE_INSTANCE_NAME


class PointCaptureProps(BaseModel):
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
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            return await self.__find_point(session)
