from typing import Optional, Sequence
from copy import copy
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import time

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
from utils.patterns import (
    AbstractBaseEntity,
    ICreateRepository,
    IDeleteRepository,
    IFindManyRepository,
    IFindRepository,
    IUpdateRepository,
)
from utils.exceptions import ModelNotFound


class RouteCreationProps(AbstractBaseEntity):
    company: Company

    description: str

    opening_time: time

    closing_time: time

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

    opening_time: time

    closing_time: time

    points: Sequence[Point]

    instance: Optional[Route] = None


class RouteExclusionProps(AbstractBaseEntity):
    uuid: str

    instance: Optional[Route] = None


class RouteService:
    def __init__(self) -> None:
        self.__company_service: CompanyService = CompanyService()

        self.__point_service: PointService = PointService()

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

    async def __find_route_by_uuid(
        self, route_uuid: str, session: AsyncSession
    ) -> Optional[Route]:
        route_repository: IFindRepository[
            RouteCaptureRepositoryProps, Route
        ] = RouteRepository(session)

        route_props: RouteCaptureRepositoryProps = RouteCaptureProps(uuid=route_uuid)

        return await route_repository.find(route_props)

    async def find_route(self, route_uuid: str) -> Optional[Route]:
        async with database.create_async_session() as session:
            return await self.__find_route_by_uuid(route_uuid, session)

    async def find_routes(
        self,
        company_uuid: Optional[str] = None,
        company_instance: Optional[Company] = None,
    ) -> Sequence[Route]:
        async with database.create_async_session() as session:
            route_repository: IFindManyRepository[
                RouteListingRepositoryProps, Route
            ] = RouteRepository(session)

            company: Company = await self.__get_company(company_uuid, company_instance)

            route_props: RouteListingRepositoryProps = RouteListingProps(
                company=company
            )

            return await route_repository.find_many(route_props)

    async def create_route(
        self,
        description: str,
        opening_time: time,
        closing_time: time,
        point_uuids: Sequence[str],
        company_uuid: Optional[str] = None,
        company_instance: Optional[Company] = None,
    ) -> Optional[Route]:
        async with database.create_async_session() as session:
            route_repository: ICreateRepository[
                RouteCreationRepositoryProps, Optional[Route]
            ] = RouteRepository(session)

            company: Company = await self.__get_company(company_uuid, company_instance)

            points: Sequence[Point] = await self.__find_points(company, point_uuids)

            route_props: RouteCreationRepositoryProps = RouteCreationProps(
                company=company,
                points=points,
                description=description,
                opening_time=opening_time,
                closing_time=closing_time,
            )

            route: Optional[Route] = await route_repository.create(route_props)

            await session.commit()

            return route

    async def update_route(
        self,
        route_uuid: str,
        description: str,
        opening_time: time,
        closing_time: time,
        point_uuids: Sequence[str],
        route_instance: Optional[Route] = None,
    ) -> Optional[Route]:
        async with database.create_async_session() as session:
            route_repository: IUpdateRepository[
                RouteUpdateRepositoryProps, Optional[Route]
            ] = RouteRepository(session)

            route: Optional[Route] = route_instance or await self.__find_route_by_uuid(
                route_uuid, session
            )

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
                opening_time=opening_time,
                closing_time=closing_time,
            )

            route = await route_repository.update(route_props)

            await session.commit()

            await session.refresh(route)

            return route

    async def delete_route(
        self, route_uuid: str, route_instance: Optional[Route] = None
    ) -> Optional[Route]:
        async with database.create_async_session() as session:
            route_repository: IDeleteRepository[
                RouteExclusionRepositoryProps, Optional[Route]
            ] = RouteRepository(session)

            route_props: RouteExclusionRepositoryProps = RouteExclusionProps(
                uuid=route_uuid, instance=route_instance
            )

            route: Optional[Route] = await route_repository.delete(route_props)

            await session.commit()

            if route is not None:
                return copy(route)
