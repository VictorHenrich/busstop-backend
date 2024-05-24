from typing import Any, Mapping, Optional, Protocol, Sequence, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    Update,
    update,
    Delete,
    delete,
    Select,
    select,
    insert,
    Insert,
)

from models import Point, Company, Route, RoutePointRelationship
from utils.patterns import (
    BaseRepository,
    CreateRepository,
    UpdateRepository,
    DeleteRepository,
    FindRepository,
    FindManyRepository,
)


class RouteCreationRepositoryProps(Protocol):
    company: Company

    description: str

    points: Sequence[Point]

    capture_instance: bool = True


class RouteUpdateRepositoryProps(Protocol):
    uuid: str

    description: str

    points: Sequence[Point]

    route_instance: Optional[Route] = None


class RouteExclusionRepositoryProps(Protocol):
    uuid: str
    route_instance: Optional[Route] = None


class RouteCaptureRepositoryProps(Protocol):
    uuid: str


class RouteListingRepositoryProps(Protocol):
    company: Company


class RouteRepository(
    BaseRepository[AsyncSession],
    CreateRepository[RouteCreationRepositoryProps, Optional[Route]],
    UpdateRepository[RouteUpdateRepositoryProps, Optional[Route]],
    DeleteRepository[RouteExclusionRepositoryProps, Optional[Route]],
    FindRepository[RouteCaptureRepositoryProps, Point],
    FindManyRepository[RouteListingRepositoryProps, Point],
):
    async def create(self, props: RouteCreationRepositoryProps) -> Optional[Route]:
        if props.capture_instance:
            route: Route = Route()

            route.company_id = props.company.id
            route.description = props.description

            for point in props.points:
                route.points.add(point)

            self.session.add(route)

            await self.session.refresh(route)

            return route

        else:
            query_route: Insert = (
                insert(Route)
                .values(company_id=props.company.id, description=props.description)
                .returning(Route)
            )

            new_route: Optional[Route] = await self.session.scalar(query_route)

            if not new_route:
                return

            query_route_point: Insert = insert(RoutePointRelationship).values(
                [
                    {"route_id": new_route.id, "point_id": point.id}
                    for point in props.points
                ]
            )

            await self.session.execute(query_route_point)

            return new_route

    async def update(self, props: RouteUpdateRepositoryProps) -> Optional[Route]:
        data: Mapping[str, Any] = {"description": props.description}

        if props.route_instance:
            for point_prop_name in dir(props.route_instance):
                for data_prop_name, data_value in data.items():
                    if point_prop_name == data_prop_name:
                        setattr(props.route_instance, data_prop_name, data_value)

            for point in props.points:
                props.route_instance.points.add(point)

            self.session.add(props.route_instance)

            await self.session.refresh(props.route_instance)

            return props.route_instance

        else:
            query_route: Update = (
                update(Route)
                .where(Route.uuid == props.uuid)
                .values(description=props.description)
                .returning(Route)
            )

            route: Optional[Route] = await self.session.scalar(query_route)

            if not route:
                return

            query_route_point: Insert = insert(RoutePointRelationship).values(
                [{"route_id": route.id, "point_id": point.id} for point in props.points]
            )

            await self.session.execute(query_route_point)

            return route

    async def delete(self, props: RouteExclusionRepositoryProps) -> Optional[Route]:
        if props.route_instance:
            for point in props.route_instance.points:
                props.route_instance.points.remove(point)

            await self.session.delete(props.route_instance)

        else:
            query_route_point: Delete = delete(RoutePointRelationship).where(
                Route.uuid == props.uuid
            )

            await self.session.execute(query_route_point)

            query_route = delete(Route).where(Route.uuid == props.uuid).returning(Route)

            return await self.session.scalar(query_route)

    async def find(self, props: RouteCaptureRepositoryProps) -> Optional[Point]:
        query: Select = select(Route).where(Route.uuid == props.uuid)

        return await self.session.scalar(query)

    async def find_many(self, props: RouteListingRepositoryProps) -> Sequence[Point]:
        query: Select = (
            select(Route)
            .join(Company, Route.company_id == Company.id)
            .where(Company.uuid == props.company.uuid)
        )

        return (await self.session.scalars(query)).all()
