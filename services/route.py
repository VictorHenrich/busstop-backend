from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from copy import copy

from models import Route, Company, Point, database
from repositories.route import (
    RouteRepository,
    RouteCaptureRepositoryProps,
    RouteListingRepositoryProps,
    RouteCreationRepositoryProps,
    RouteUpdateRepositoryProps,
    RouteExclusionRepositoryProps,
)
from services.company import CompanyService
from services.point import PointService
from utils.patterns import AbstractBaseEntity
from utils.exceptions import ModelNotFound


class RouteCreationProps(AbstractBaseEntity):
    company: Company

    description: str

    points: Sequence[Point]


class RouteListingProps(AbstractBaseEntity):
    company: Company


class CompanyCaptureProps(AbstractBaseEntity):
    uuid: str


class RouteCaptureProps(AbstractBaseEntity):
    uuid: str


class RouteUpdateProps(AbstractBaseEntity):
    uuid: str

    description: str

    points: Sequence[Point]

    instance: Optional[Route] = None


class RouteExclusionProps(AbstractBaseEntity):
    uuid: str

    instance: Optional[Route] = None


class RouteService:
    def __init__(self) -> None:
        self.__session: AsyncSession = database.create_async_session()

        self.__company_service: CompanyService = CompanyService()

        self.__point_service: PointService = PointService()

        self.__route_repository: RouteRepository = RouteRepository(self.__session)

    async def __get_company(
        self, company_uuid: Optional[str], company_instance: Optional[Company]
    ):
        if company_instance is None:
            return await self.__company_service.find_company(company_uuid or "")

        else:
            return company_instance

    async def __find_points(
        self, company: Company, point_uuids: Sequence[str]
    ) -> Sequence[Point]:
        return await self.__point_service.find_points(
            point_uuids=point_uuids, company_instance=company
        )

    async def find_route(self, route_uuid: str) -> Optional[Route]:
        async with self.__session:
            route_props: RouteCaptureRepositoryProps = RouteCaptureProps(
                uuid=route_uuid
            )

            return await self.__route_repository.find(route_props)

    async def find_routes(
        self,
        company_uuid: Optional[str] = None,
        company_instance: Optional[Company] = None,
    ) -> Sequence[Route]:
        async with self.__session:
            company: Company = await self.__get_company(company_uuid, company_instance)

            route_props: RouteListingRepositoryProps = RouteListingProps(
                company=company
            )

            return await self.__route_repository.find_many(route_props)

    async def create_route(
        self,
        description: str,
        point_uuids: Sequence[str],
        company_uuid: Optional[str] = None,
        company_instance: Optional[Company] = None,
    ) -> Optional[Route]:
        async with self.__session:
            company: Company = await self.__get_company(company_uuid, company_instance)

            points: Sequence[Point] = await self.__find_points(company, point_uuids)

            route_props: RouteCreationRepositoryProps = RouteCreationProps(
                company=company, points=points, description=description
            )

            return await self.__route_repository.create(route_props)

    async def update_route(
        self,
        route_uuid: str,
        description: str,
        point_uuids: Sequence[str],
        route_instance: Optional[Route] = None,
    ) -> Optional[Route]:
        async with self.__session:
            route: Optional[Route] = route_instance or await self.find_route(route_uuid)

            if not route:
                raise ModelNotFound(Route, route_uuid)

            points: Sequence[Point] = await self.__find_points(
                route.company, point_uuids
            )

            route_props: RouteUpdateRepositoryProps = RouteUpdateProps(
                uuid=route_uuid,
                points=points,
                description=description,
                instance=route_instance,
            )

            route = await self.__route_repository.update(route_props)

            await self.__session.commit()

            await self.__session.refresh(route)

    async def delete_route(
        self, route_uuid: str, route_instance: Optional[Route] = None
    ) -> Optional[Route]:
        async with self.__session:
            route_props: RouteExclusionRepositoryProps = RouteExclusionProps(
                uuid=route_uuid, instance=route_instance
            )

            route: Optional[Route] = await self.__route_repository.delete(route_props)

            if route is not None:
                return copy(route)
