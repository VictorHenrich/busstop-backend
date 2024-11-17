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
from utils.exceptions import ModelNotFound


class IRouteCreateRepository(Protocol):
    company: Company

    description: str

    opening_time: time

    closing_time: time

    ticket_price: float

    points: Sequence[Point]


class IRouteUpdateRepository(Protocol):
    uuid: str

    description: str

    points: Sequence[Point]

    opening_time: time

    closing_time: time

    ticket_price: float

    instance: Optional[Route] = None


class IRouteDeleteRepository(Protocol):
    uuid: str

    instance: Optional[Route] = None


class IRouteFindRepository(Protocol):
    uuid: str


class IRouteFindManyRepository(Protocol):
    company: Company


class RouteRepository(
    BaseRepository[AsyncSession],
    ICreateRepository[IRouteCreateRepository, Optional[Route]],
    IUpdateRepository[IRouteUpdateRepository, Optional[Route]],
    IDeleteRepository[IRouteDeleteRepository, Optional[Route]],
    IFindRepository[IRouteFindRepository, Route],
    IFindManyRepository[IRouteFindManyRepository, Route],
):
    async def create(self, props: IRouteCreateRepository) -> Optional[Route]:
        route: Route = Route()

        route.company_id = props.company.id
        route.description = props.description
        route.opening_time = props.opening_time
        route.closing_time = props.closing_time
        route.ticket_price = props.ticket_price

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

    async def update(self, props: IRouteUpdateRepository) -> Optional[Route]:
        if props.instance:
            props.instance.description = props.description

            props.instance.opening_time = props.opening_time

            props.instance.closing_time = props.closing_time

            props.instance.ticket_price = props.ticket_price

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
                    ticket_price=props.ticket_price,
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

    async def delete(self, props: IRouteDeleteRepository) -> Optional[Route]:
        if props.instance:
            for point in props.instance.points:
                props.instance.points.remove(point)

            await self.session.delete(props.instance)

            return props.instance

        else:
            route: Optional[Route] = await self.session.scalar(
                select(Route).where(Route.uuid == props.uuid)
            )

            if not route:
                raise ModelNotFound(Route, props.uuid)

            query_route_point: Delete = delete(RoutePoint).where(
                RoutePoint.route_id == route.id
            )

            await self.session.execute(query_route_point)

            await self.session.delete(route)

            return route

    async def find(self, props: IRouteFindRepository) -> Optional[Route]:
        query: Select = (
            select(Route)
            .options(joinedload(Route.company))
            .where(Route.uuid == props.uuid)
        )

        return await self.session.scalar(query)

    async def find_many(self, props: IRouteFindManyRepository) -> Sequence[Route]:
        query: Select = (
            select(Route)
            .join(Company, Route.company_id == Company.id)
            .options(joinedload(Route.company))
            .where(Company.uuid == props.company.uuid)
        )

        return (await self.session.scalars(query)).all()
