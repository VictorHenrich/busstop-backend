from typing import Optional, Protocol, Sequence, Mapping, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update, update, Delete, delete, Select, select, insert, Insert

from models import Point, Company
from utils.patterns import (
    BaseRepository,
    CreateRepository,
    UpdateRepository,
    DeleteRepository,
    FindRepository,
    FindManyRepository,
)


class PointCreationRepositoryProps(Protocol):
    company_id: int

    address_state: str

    address_city: str

    address_neighborhood: str

    address_street: str

    address_number: str

    latitude: str

    longitude: str


class PointUpdateRepositoryProps(Protocol):
    uuid: str

    address_state: Optional[str]

    address_city: Optional[str]

    address_neighborhood: Optional[str]

    address_street: Optional[str]

    address_number: Optional[str]

    latitude: Optional[str]

    longitude: Optional[str]


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
    DeleteRepository[PointExclusionRepositoryProps, None],
    FindRepository[PointCaptureRepositoryProps, Point],
    FindManyRepository[PointListingRepositoryProps, Point],
):
    async def create(self, props: PointCreationRepositoryProps) -> Optional[Point]:
        query: Insert = (
            insert(Point)
            .values(
                company_id=props.company_id,
                address_state=props.address_state,
                address_city=props.address_city,
                address_neighborhood=props.address_neighborhood,
                address_street=props.address_street,
                address_number=props.address_number,
                latitude=props.latitude,
                longitude=props.longitude,
            )
            .returning()
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

        query: Update = (
            update(Point)
            .where(Point.uuid == props.uuid)
            .values(
                **{name: value for name, value in data.items() if value is not None}
            )
            .returning()
        )

        return await self.session.scalar(query)

    async def delete(self, props: PointExclusionRepositoryProps) -> None:
        query: Delete = delete(Point).where(Point.uuid == props.uuid)

        await self.session.execute(query)

    async def find(self, props: PointCaptureRepositoryProps) -> Optional[Point]:
        query: Select = select(Point).where(Point.uuid == props.uuid)

        return await self.session.scalar(query)

    async def find_many(self, props: PointListingRepositoryProps) -> Sequence[Point]:
        query: Select = select(Point).where(Company.uuid == props.company_uuid)

        return list(await self.session.scalars(query))
