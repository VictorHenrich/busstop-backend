from typing import Optional, Protocol, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update, update, Delete, delete, Select, select, insert, Insert
from sqlalchemy.orm import joinedload
from datetime import time

from models import Route, Point, Company, RoutePoint
from utils.patterns import (
    BaseRepository,
    ICreateRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindRepository,
    IFindManyRepository,
)


class RouteCreationRepositoryProps(Protocol):
    company: Company

    description: str

    opening_time: time

    closing_time: time

    points: Sequence[Point]


class RouteUpdateRepositoryProps(Protocol):
    uuid: str

    description: str

    points: Sequence[Point]

    opening_time: time

    closing_time: time

    instance: Optional[Route] = None


class RouteExclusionRepositoryProps(Protocol):
    uuid: str

    instance: Optional[Route] = None


class RouteCaptureRepositoryProps(Protocol):
    uuid: str


class RouteListingRepositoryProps(Protocol):
    company: Company


class RouteRepository(
    BaseRepository[AsyncSession],
    ICreateRepository[RouteCreationRepositoryProps, Optional[Route]],
    IUpdateRepository[RouteUpdateRepositoryProps, Optional[Route]],
    IDeleteRepository[RouteExclusionRepositoryProps, Optional[Route]],
    IFindRepository[RouteCaptureRepositoryProps, Route],
    IFindManyRepository[RouteListingRepositoryProps, Route],
):
    async def create(self, props: RouteCreationRepositoryProps) -> Optional[Route]:
        route: Route = Route()

        route.company_id = props.company.id
        route.description = props.description
        route.opening_time = props.opening_time
        route.closing_time = props.closing_time

        for index in range(len(props.points)):
            route.points.add(
                RoutePoint(index=index, route=route, point=props.points[index])
            )

        self.session.add(route)

        return route

        # query_route: Insert = (
        #     insert(Route)
        #     .values(company_id=props.company.id, description=props.description)
        #     .returning(Route)
        # )

        # new_route: Optional[Route] = await self.session.scalar(query_route)

        # if not new_route:
        #     return

        # query_route_point: Insert = insert(RoutePointRelationship).values(
        #     [
        #         {"route_id": new_route.id, "point_id": point.id}
        #         for point in props.points
        #     ]
        # )

        # await self.session.execute(query_route_point)

        # return new_route

    async def update(self, props: RouteUpdateRepositoryProps) -> Optional[Route]:
        if props.instance:
            props.instance.description = props.description

            props.instance.opening_time = props.opening_time

            props.instance.closing_time = props.closing_time

            for index in range(len(props.points)):
                props.instance.points.add(
                    RoutePoint(
                        index=index, route=props.instance, point=props.points[index]
                    )
                )

            self.session.add(props.instance)

            return props.instance

        else:
            query_route: Update = (
                update(Route)
                .where(Route.uuid == props.uuid)
                .values(
                    description=props.description,
                    opening_time=props.opening_time,
                    closing_time=props.closing_time,
                )
                .returning(Route)
            )

            route: Optional[Route] = await self.session.scalar(query_route)

            if not route:
                return

            query_route_point: Insert = insert(RoutePoint).values(
                [
                    {
                        "route_id": route.id,
                        "point_id": props.points[index].id,
                        "index": index,
                    }
                    for index in range(len(props.points))
                ]
            )

            await self.session.execute(query_route_point)

            return route

    async def delete(self, props: RouteExclusionRepositoryProps) -> Optional[Route]:
        if props.instance:
            for point in props.instance.points:
                props.instance.points.remove(point)

            await self.session.delete(props.instance)

            return props.instance

        else:
            query_route_point: Delete = delete(RoutePoint).where(
                Route.uuid == props.uuid
            )

            await self.session.execute(query_route_point)

            query_route = delete(Route).where(Route.uuid == props.uuid).returning(Route)

            return await self.session.scalar(query_route)

    async def find(self, props: RouteCaptureRepositoryProps) -> Optional[Route]:
        query: Select = (
            select(Route)
            .options(joinedload(Route.company))
            .where(Route.uuid == props.uuid)
        )

        return await self.session.scalar(query)

    async def find_many(self, props: RouteListingRepositoryProps) -> Sequence[Route]:
        query: Select = (
            select(Route)
            .join(Company, Route.company_id == Company.id)
            .options(joinedload(Route.company))
            .where(Company.uuid == props.company.uuid)
        )

        return (await self.session.scalars(query)).all()
