from typing import Optional, Sequence
from copy import copy
from pyspark.sql import SparkSession, DataFrame

from models import Company, Point, database
from repositories.point import (
    PointRepository,
    IPointCreateRepository,
    IPointUpdateRepository,
    IPointDeleteRepository,
    IPointFindRepository,
    IPointFindManyRepository,
)
from services.company import CompanyService
from services.geolocation import GeoLocationService
from utils.spark import SparkUtils
from utils.patterns import (
    AbstractBaseEntity,
    ICreateRepository,
    IDeleteRepository,
    IFindManyRepository,
    IFindRepository,
    IUpdateRepository,
)


class PointCreationProps(AbstractBaseEntity):
    address_zip_code: str

    address_state: str

    address_city: str

    address_neighborhood: str

    address_street: str

    address_number: str

    latitude: str

    longitude: str

    company: Company

    place_id: Optional[str] = None


class PointUpdateProps(AbstractBaseEntity):
    uuid: str

    address_zip_code: str

    address_state: str

    address_city: str

    address_neighborhood: str

    address_street: str

    address_number: str

    latitude: str

    longitude: str

    instance: Optional[Point] = None

    place_id: Optional[str] = None


class PointExclusionProps(AbstractBaseEntity):
    uuid: str


class PointCaptureProps(AbstractBaseEntity):
    uuid: str


class PointListingProps(AbstractBaseEntity):
    company: Company

    uuids: Sequence[str]


class PointService:
    def __init__(self) -> None:
        self.__company_service: CompanyService = CompanyService()

        self.__geolocation_service: GeoLocationService = GeoLocationService()

    async def __get_company(
        self, company_uuid: Optional[str], company_instance: Optional[Company]
    ):
        if company_instance is None:
            return await self.__company_service.find_company(company_uuid or "")

        else:
            return company_instance

    async def create_point(
        self,
        address_zip_code: str,
        address_state: str,
        address_city: str,
        address_neighborhood: str,
        address_street: str,
        address_number: str,
        latitude: str,
        longitude: str,
        place_id: Optional[str] = None,
        company_instance: Optional[Company] = None,
        company_uuid: Optional[str] = None,
    ) -> Optional[Point]:
        async with database.create_async_session() as session:
            point_repository: ICreateRepository[
                IPointCreateRepository, Optional[Point]
            ] = PointRepository(session)

            company: Company = await self.__get_company(company_uuid, company_instance)

            point_props: IPointCreateRepository = PointCreationProps(
                address_zip_code=address_zip_code,
                address_state=address_state,
                address_city=address_city,
                address_neighborhood=address_neighborhood,
                address_street=address_street,
                address_number=address_number,
                latitude=latitude,
                longitude=longitude,
                place_id=place_id,
                company=company,
            )

            point: Optional[Point] = await point_repository.create(point_props)

            await session.commit()

            return point

    async def update_point(
        self,
        point_uuid: str,
        address_zip_code: str,
        address_state: str,
        address_city: str,
        address_neighborhood: str,
        address_street: str,
        address_number: str,
        latitude: str,
        longitude: str,
        place_id: Optional[str] = None,
        point_instance: Optional[Point] = None,
    ) -> Optional[Point]:
        uuid: str = point_uuid

        if point_instance is not None:
            uuid = point_instance.uuid

        async with database.create_async_session() as session:
            point_repository: IUpdateRepository[
                IPointUpdateRepository, Optional[Point]
            ] = PointRepository(session)

            point_props: IPointUpdateRepository = PointUpdateProps(
                address_zip_code=address_zip_code,
                instance=point_instance,
                address_state=address_state,
                address_city=address_city,
                address_neighborhood=address_neighborhood,
                address_street=address_street,
                address_number=address_number,
                latitude=latitude,
                longitude=longitude,
                place_id=place_id,
                uuid=uuid,
            )

            point: Optional[Point] = await point_repository.update(point_props)

            await session.commit()
            await session.refresh(point)

            return point

    async def delete_point(self, point_uuid: str) -> Optional[Point]:
        async with database.create_async_session() as session:
            point_repository: IDeleteRepository[
                IPointDeleteRepository, Optional[Point]
            ] = PointRepository(session)

            point_props: IPointDeleteRepository = PointExclusionProps(uuid=point_uuid)

            point: Optional[Point] = await point_repository.delete(point_props)

            await session.commit()

            if point is not None:
                return copy(point)

    async def find_point(self, point_uuid: str) -> Optional[Point]:
        async with database.create_async_session() as session:
            point_repository: IFindRepository[IPointFindRepository, Point] = (
                PointRepository(session)
            )

            point_props: IPointFindRepository = PointCaptureProps(uuid=point_uuid)

            return await point_repository.find(point_props)

    async def find_points(
        self,
        point_uuids: Sequence[str],
        company_instance: Optional[Company] = None,
        company_uuid: Optional[str] = None,
    ) -> Sequence[Point]:
        async with database.create_async_session() as session:
            point_repository: IFindManyRepository[IPointFindManyRepository, Point] = (
                PointRepository(session)
            )

            company: Company = await self.__get_company(company_uuid, company_instance)

            point_props: IPointFindManyRepository = PointListingProps(
                company=company, uuids=point_uuids
            )

            return await point_repository.find_many(point_props)

    async def find_points_closer(
        self, origin: Point, distance: float = 0, company_uuids: Sequence[str] = []
    ):
        spark_session: SparkSession = SparkUtils.create_session_for_database(
            "PointCloserSpark"
        )

        spark_session.createDataFrame([["a", 1], ["b", 2], ["c", 3]]).show()

        spark_session.stop()

        # point_dataframe: DataFrame = SparkUtils.create_dataframe_for_table(
        #     database=database, table=Point, spark_session=spark_session
        # )

        # company_dataframe: DataFrame = SparkUtils.create_dataframe_for_table(
        #     database=database, table=Company, spark_session=spark_session
        # )

        # company_dataframe = company_dataframe.filter(
        #     company_dataframe["uuid"].isin(company_uuids)
        # )

        # point_company_dataframe = point_dataframe.join(
        #     company_dataframe, point_dataframe["company_id"] == company_dataframe["id"]
        # )

        # point_company_dataframe.show()

        # spark_session.stop()

        return []
