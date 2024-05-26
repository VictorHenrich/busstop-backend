from typing import Optional, Protocol, Sequence, Mapping, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update, update, Delete, delete, Select, select, insert, Insert

from models import Point, Company, RoutePointRelationship
from utils.patterns import (
    BaseRepository,
    ICreateRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindRepository,
    IFindManyRepository,
)


class PointCreationRepositoryProps(Protocol):
    company: Company

    address_state: str

    address_city: str

    address_neighborhood: str

    address_street: str

    address_number: str

    latitude: str

    longitude: str


class PointUpdateRepositoryProps(Protocol):
    uuid: str

    address_state: str

    address_city: str

    address_neighborhood: str

    address_street: str

    address_number: str

    latitude: str

    longitude: str

    point_instance: Optional[Point] = None


class PointExclusionRepositoryProps(Protocol):
    uuid: str


class PointCaptureRepositoryProps(Protocol):
    uuid: str


class PointListingRepositoryProps(Protocol):
    company: Company
    uuids: Sequence[str] = []


class PointRepository(
    BaseRepository[AsyncSession],
    ICreateRepository[PointCreationRepositoryProps, Optional[Point]],
    IUpdateRepository[PointUpdateRepositoryProps, Optional[Point]],
    IDeleteRepository[PointExclusionRepositoryProps, Optional[Point]],
    IFindRepository[PointCaptureRepositoryProps, Point],
    IFindManyRepository[PointListingRepositoryProps, Point],
):
    async def create(self, props: PointCreationRepositoryProps) -> Optional[Point]:
        point: Point = Point()

        point.company_id = props.company.id
        point.address_state = props.address_state
        point.address_city = props.address_city
        point.address_neighborhood = props.address_neighborhood
        point.address_street = props.address_street
        point.address_number = props.address_number
        point.latitude = props.latitude
        point.longitude = props.longitude

        self.session.add(point)

        return point

        # else:
        #     query: Insert = (
        #         insert(Point)
        #         .values(
        #             company_id=props.company.id,
        #             address_state=props.address_state,
        #             address_city=props.address_city,
        #             address_neighborhood=props.address_neighborhood,
        #             address_street=props.address_street,
        #             address_number=props.address_number,
        #             latitude=props.latitude,
        #             longitude=props.longitude,
        #         )
        #         .returning(Point)
        #     )

        #     return await self.session.scalar(query)

    async def update(self, props: PointUpdateRepositoryProps) -> Optional[Point]:
        data: Mapping[str, Any] = {
            "address_state": props.address_state,
            "address_city": props.address_city,
            "address_neighborhood": props.address_neighborhood,
            "address_street": props.address_street,
            "address_number": props.address_number,
            "latitude": props.latitude,
            "longitude": props.longitude,
        }

        data = {name: value for name, value in data.items() if value is not None}

        if props.point_instance:
            props.point_instance.address_state = props.address_state
            props.point_instance.address_city = props.address_city
            props.point_instance.address_neighborhood = props.address_neighborhood
            props.point_instance.address_street = props.address_street
            props.point_instance.address_number = props.address_number
            props.point_instance.latitude = props.latitude
            props.point_instance.longitude = props.longitude

            self.session.add(props.point_instance)

            return props.point_instance

        else:
            query: Update = (
                update(Point)
                .where(Point.uuid == props.uuid)
                .values(**data)
                .returning(Point)
            )

            return await self.session.scalar(query)

    async def delete(self, props: PointExclusionRepositoryProps) -> Optional[Point]:
        query_route_point: Delete = delete(RoutePointRelationship).where(
            Point.uuid == props.uuid
        )

        await self.session.execute(query_route_point)

        query_route = delete(Point).where(Point.uuid == props.uuid).returning(Point)

        return await self.session.scalar(query_route)

    async def find(self, props: PointCaptureRepositoryProps) -> Optional[Point]:
        query: Select = select(Point).where(Point.uuid == props.uuid)

        return await self.session.scalar(query)

    async def find_many(self, props: PointListingRepositoryProps) -> Sequence[Point]:
        query: Select = select(Point).where(Point.company_id == props.company.id)

        if props.uuids:
            query.where(Point.uuid.in_(props.uuids))

        return (await self.session.scalars(query)).all()
