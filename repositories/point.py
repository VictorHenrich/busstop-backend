from typing import Optional, Protocol, Sequence, Mapping, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update, update, Delete, delete, Select, select, insert, Insert

from models import Point, Company, RoutePoint
from utils.patterns import (
    BaseRepository,
    ICreateRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindRepository,
    IFindManyRepository,
)


class IPointCreateRepository(Protocol):
    company: Company

    address_zip_code: str

    address_state: str

    address_city: str

    address_neighborhood: str

    address_street: str

    address_number: str

    latitude: str

    longitude: str


class IPointUpdateRepository(Protocol):
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


class IPointDeleteRepository(Protocol):
    uuid: str


class IPointFindRepository(Protocol):
    uuid: str


class IPointFindManyRepository(Protocol):
    company: Company
    uuids: Sequence[str] = []


class PointRepository(
    BaseRepository[AsyncSession],
    ICreateRepository[IPointCreateRepository, Optional[Point]],
    IUpdateRepository[IPointUpdateRepository, Optional[Point]],
    IDeleteRepository[IPointDeleteRepository, Optional[Point]],
    IFindRepository[IPointFindRepository, Point],
    IFindManyRepository[IPointFindManyRepository, Point],
):
    async def create(self, props: IPointCreateRepository) -> Optional[Point]:
        point: Point = Point()

        point.company_id = props.company.id
        point.address_state = props.address_state
        point.address_city = props.address_city
        point.address_neighborhood = props.address_neighborhood
        point.address_street = props.address_street
        point.address_number = props.address_number
        point.address_zip_code = props.address_zip_code
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

    async def update(self, props: IPointUpdateRepository) -> Optional[Point]:
        if props.instance:
            props.instance.address_state = props.address_state
            props.instance.address_zip_code = props.address_zip_code
            props.instance.address_city = props.address_city
            props.instance.address_neighborhood = props.address_neighborhood
            props.instance.address_street = props.address_street
            props.instance.address_number = props.address_number
            props.instance.latitude = props.latitude
            props.instance.longitude = props.longitude

            self.session.add(props.instance)

            return props.instance

        else:
            data: Mapping[str, Any] = {
                "address_zip_code": props.address_zip_code,
                "address_state": props.address_state,
                "address_city": props.address_city,
                "address_neighborhood": props.address_neighborhood,
                "address_street": props.address_street,
                "address_number": props.address_number,
                "latitude": props.latitude,
                "longitude": props.longitude,
            }

            data = {name: value for name, value in data.items() if value is not None}

            query: Update = (
                update(Point)
                .where(Point.uuid == props.uuid)
                .values(**data)
                .returning(Point)
            )

            return await self.session.scalar(query)

    async def delete(self, props: IPointDeleteRepository) -> Optional[Point]:
        query_route_point: Delete = delete(RoutePoint).where(Point.uuid == props.uuid)

        await self.session.execute(query_route_point)

        query_route = delete(Point).where(Point.uuid == props.uuid).returning(Point)

        return await self.session.scalar(query_route)

    async def find(self, props: IPointFindRepository) -> Optional[Point]:
        query: Select = select(Point).where(Point.uuid == props.uuid)

        return await self.session.scalar(query)

    async def find_many(self, props: IPointFindManyRepository) -> Sequence[Point]:
        query: Select = select(Point).where(Point.company_id == props.company.id)

        if props.uuids:
            query.where(Point.uuid.in_(props.uuids))

        return (await self.session.scalars(query)).all()
