from typing import Optional, Protocol, Sequence, Mapping, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update, update, Delete, delete, Select, select, insert, Insert

from models import Company
from utils.patterns import (
    BaseRepository,
    ICreateRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindManyRepository,
)


class CompanyCreationRepositoryProps(Protocol):
    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class CompanyUpdateRepositoryProps(Protocol):
    uuid: str

    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class CompanyExclusionRepositoryProps(Protocol):
    uuid: str


class CompanyListingRepositoryProps(Protocol):
    company_name: Optional[str]


class CompanyRepository(
    BaseRepository[AsyncSession],
    ICreateRepository[CompanyCreationRepositoryProps, None],
    IUpdateRepository[CompanyUpdateRepositoryProps, None],
    IDeleteRepository[CompanyExclusionRepositoryProps, None],
    IFindManyRepository[CompanyListingRepositoryProps, Company],
):
    async def create(self, props: CompanyCreationRepositoryProps) -> None:
        query: Insert = insert(Company).values(
            company_name=props.company_name,
            fantasy_name=props.fantasy_name,
            document_cnpj=props.document_cnpj,
            email=props.email,
        )

        await self.session.execute(query)

    async def update(self, props: CompanyUpdateRepositoryProps) -> None:
        query: Update = (
            update(Company)
            .where(Company.uuid == props.uuid)
            .values(
                company_name=props.company_name,
                fantasy_name=props.fantasy_name,
                document_cnpj=props.document_cnpj,
                email=props.email,
            )
        )

        await self.session.execute(query)

    async def delete(self, props: CompanyExclusionRepositoryProps) -> None:
        query: Delete = delete(Company).where(Company.uuid == props.uuid)

        await self.session.execute(query)

    async def find_many(
        self, props: CompanyListingRepositoryProps
    ) -> Sequence[Company]:
        query_filter: Mapping[str, Any] = {}

        query: Select = select(Company).where(**query_filter)

        return (await self.session.scalars(query)).all()
