from typing import Optional, Protocol, Sequence, Mapping, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update, update, Delete, delete, Select, select, insert, Insert

from models import Company
from utils.patterns import (
    BaseRepository,
    ICreateRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindRepository,
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

    instance: Optional[Company] = None


class CompanyExclusionRepositoryProps(Protocol):
    uuid: str

    instance: Optional[Company] = None


class CompanyCaptureRepositoryProps(Protocol):
    uuid: str


class CompanyListingRepositoryProps(Protocol):
    company_name: Optional[str]

    limit: int = 50

    page: int = 0


class CompanyRepository(
    BaseRepository[AsyncSession],
    ICreateRepository[CompanyCreationRepositoryProps, Optional[Company]],
    IUpdateRepository[CompanyUpdateRepositoryProps, Optional[Company]],
    IDeleteRepository[CompanyExclusionRepositoryProps, Optional[Company]],
    IFindManyRepository[CompanyListingRepositoryProps, Company],
    IFindRepository[CompanyCaptureRepositoryProps, Company],
):
    async def create(self, props: CompanyCreationRepositoryProps) -> Optional[Company]:
        query: Insert = insert(Company).values(
            company_name=props.company_name,
            fantasy_name=props.fantasy_name,
            document_cnpj=props.document_cnpj,
            email=props.email,
        )

        return await self.session.scalar(query)

    async def update(self, props: CompanyUpdateRepositoryProps) -> Optional[Company]:
        if props.instance is not None:
            props.instance.company_name = props.company_name
            props.instance.fantasy_name = props.fantasy_name
            props.instance.document_cnpj = props.document_cnpj
            props.instance.email = props.email

            self.session.add(props.instance)

            return props.instance

        else:
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

            return await self.session.scalar(query)

    async def delete(self, props: CompanyExclusionRepositoryProps) -> Optional[Company]:
        if props.instance is not None:
            await self.session.delete(props.instance)

            return props.instance

        else:
            query: Delete = delete(Company).where(Company.uuid == props.uuid)

            return await self.session.scalar(query)

    async def find(self, props: CompanyCaptureRepositoryProps) -> Optional[Company]:
        query: Select = select(Company).where(Company.uuid == props.uuid)

        return await self.session.scalar(query)

    async def find_many(
        self, props: CompanyListingRepositoryProps
    ) -> Sequence[Company]:
        query_filter: Mapping[str, Any] = {}

        query: Select = (
            select(Company).where(**query_filter).offset(props.page).limit(props.limit)
        )

        return (await self.session.scalars(query)).all()
