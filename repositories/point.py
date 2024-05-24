from typing import Optional, Protocol, Sequence, Mapping, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update, update, Delete, delete, Select, select, insert, Insert

from models import Point, Company, RoutePointRelationship
from utils.patterns import (
    BaseRepository,
    CreateRepository,
    UpdateRepository,
    DeleteRepository,
    FindRepository,
    FindManyRepository,
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

    capture_instance: bool = True


class PointUpdateRepositoryProps(Protocol):
    uuid: str

    address_state: Optional[str] = None

    address_city: Optional[str] = None

    address_neighborhood: Optional[str] = None

    address_street: Optional[str] = None

    address_number: Optional[str] = None

    latitude: Optional[str] = None

    longitude: Optional[str] = None

    point_instance: Optional[Point] = None


class PointExclusionRepositoryProps(Protocol):
    uuid: str


class PointCaptureRepositoryProps(Protocol):
    uuid: str


class PointListingRepositoryProps(Protocol):
    company_uuid: str


class PointRepository(
    BaseRepository[AsyncSession],
    CreateRepository[PointCreationRepositoryProps, Optional[Point]],
    UpdateRepository[PointUpdateRepositoryProps, Optional[Point]],
    DeleteRepository[PointExclusionRepositoryProps, Optional[Point]],
    FindRepository[PointCaptureRepositoryProps, Point],
    FindManyRepository[PointListingRepositoryProps, Point],
):
    async def create(self, props: PointCreationRepositoryProps) -> Optional[Point]:
        if props.capture_instance:
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

            await self.session.refresh(point)

            return point

        else:
            query: Insert = insert(Point).values(
                company_id=props.company.id,
                address_state=props.address_state,
                address_city=props.address_city,
                address_neighborhood=props.address_neighborhood,
                address_street=props.address_street,
                address_number=props.address_number,
                latitude=props.latitude,
                longitude=props.longitude,
            )

            return await self.session.scalar(query)

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
            for point_prop_name in dir(props.point_instance):
                for data_prop_name, data_value in data.items():
                    if data_prop_name == point_prop_name:
                        setattr(props.point_instance, point_prop_name, data_value)

            self.session.add(props.point_instance)

            await self.session.refresh(props.point_instance)

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
        query: Select = select(Point).where(Company.uuid == props.company_uuid)

        return (await self.session.scalars(query)).all()
