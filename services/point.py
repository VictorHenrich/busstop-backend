from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from copy import copy

from models import Company, Point, database
from repositories.point import (
    PointRepository,
    PointCreationRepositoryProps,
    PointUpdateRepositoryProps,
    PointExclusionRepositoryProps,
    PointCaptureRepositoryProps,
    PointListingRepositoryProps,
)
from services.company import CompanyService
from utils.patterns import AbstractBaseEntity


class PointCreationProps(AbstractBaseEntity):
    address_state: str

    address_city: str

    address_neighborhood: str

    address_street: str

    address_number: str

    latitude: str

    longitude: str

    company: Company


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


class PointExclusionProps(AbstractBaseEntity):
    uuid: str


class PointCaptureProps(AbstractBaseEntity):
    uuid: str


class PointListingProps(AbstractBaseEntity):
    company: Company

    uuids: Sequence[str]


class PointService:
    def __init__(self) -> None:
        self.__session: AsyncSession = database.create_async_session()

        self.__point_repository: PointRepository = PointRepository(self.__session)

        self.__company_service: CompanyService = CompanyService()

    async def __get_company(
        self, company_uuid: Optional[str], company_instance: Optional[Company]
    ):
        if company_instance is None:
            return await self.__company_service.find_company(company_uuid or "")

        else:
            return company_instance

    async def create_point(
        self,
        address_state: str,
        address_city: str,
        address_neighborhood: str,
        address_street: str,
        address_number: str,
        latitude: str,
        longitude: str,
        company_instance: Optional[Company] = None,
        company_uuid: Optional[str] = None,
    ) -> Optional[Point]:
        async with self.__session:
            company: Company = await self.__get_company(company_uuid, company_instance)

            point_props: PointCreationRepositoryProps = PointCreationProps(
                address_state=address_state,
                address_city=address_city,
                address_neighborhood=address_neighborhood,
                address_street=address_street,
                address_number=address_number,
                latitude=latitude,
                longitude=longitude,
                company=company,
            )

            point: Optional[Point] = await self.__point_repository.create(point_props)

            await self.__session.commit()

            return point

    async def update_point(
        self,
        point_uuid: str,
        address_state: str,
        address_city: str,
        address_neighborhood: str,
        address_street: str,
        address_number: str,
        latitude: str,
        longitude: str,
        point_instance: Optional[Point] = None,
    ) -> Optional[Point]:
        uuid: str = point_uuid

        if point_instance is not None:
            uuid = point_instance.uuid

        async with self.__session:
            point_props: PointUpdateRepositoryProps = PointUpdateProps(
                point_instance=point_instance,
                address_state=address_state,
                address_city=address_city,
                address_neighborhood=address_neighborhood,
                address_street=address_street,
                address_number=address_number,
                latitude=latitude,
                longitude=longitude,
                uuid=uuid,
            )

            point: Optional[Point] = await self.__point_repository.update(point_props)

            await self.__session.commit()
            await self.__session.refresh(point)

            return point

    async def delete_point(self, point_uuid: str) -> Optional[Point]:
        async with self.__session:
            point_props: PointExclusionRepositoryProps = PointExclusionProps(
                uuid=point_uuid
            )

            point: Optional[Point] = await self.__point_repository.delete(point_props)

            await self.__session.commit()

            if point is not None:
                return copy(point)

    async def find_point(self, point_uuid: str) -> Optional[Point]:
        async with self.__session:
            point_props: PointCaptureRepositoryProps = PointCaptureProps(
                uuid=point_uuid
            )

            return await self.__point_repository.find(point_props)

    async def find_points(
        self,
        point_uuids: Sequence[str],
        company_instance: Optional[Company] = None,
        company_uuid: Optional[str] = None,
    ) -> Sequence[Point]:
        async with self.__session:
            company: Company = await self.__get_company(company_uuid, company_instance)

            point_props: PointListingRepositoryProps = PointListingProps(
                company=company, uuids=point_uuids
            )

            return await self.__point_repository.find_many(point_props)
