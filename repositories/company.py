from typing import Optional, Protocol, Sequence
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
from utils.types import DictType


class ICompanyCreateRepository(Protocol):
    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class ICompanyUpdateRepository(Protocol):
    uuid: str

    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str

    instance: Optional[Company] = None


class ICompanyDeleteRepository(Protocol):
    uuid: str

    instance: Optional[Company] = None


class ICompanyFindRepository(Protocol):
    uuid: str


class ICompanyFindManyRepository(Protocol):
    company_name: Optional[str]

    limit: int = 50

    page: int = 0


class CompanyRepository(
    BaseRepository[AsyncSession],
    ICreateRepository[ICompanyCreateRepository, Optional[Company]],
    IUpdateRepository[ICompanyUpdateRepository, Optional[Company]],
    IDeleteRepository[ICompanyDeleteRepository, Optional[Company]],
    IFindManyRepository[ICompanyFindManyRepository, Company],
    IFindRepository[ICompanyFindRepository, Company],
):
    async def create(self, props: ICompanyCreateRepository) -> Optional[Company]:
        query: Insert = (
            insert(Company)
            .values(
                company_name=props.company_name,
                fantasy_name=props.fantasy_name,
                document_cnpj=props.document_cnpj,
                email=props.email,
            )
            .returning(Company)
        )

        return await self.session.scalar(query)

    async def update(self, props: ICompanyUpdateRepository) -> Optional[Company]:
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

    async def delete(self, props: ICompanyDeleteRepository) -> Optional[Company]:
        if props.instance is not None:
            await self.session.delete(props.instance)

            return props.instance

        else:
            query: Delete = delete(Company).where(Company.uuid == props.uuid)

            return await self.session.scalar(query)

    async def find(self, props: ICompanyFindRepository) -> Optional[Company]:
        query: Select = select(Company).where(Company.uuid == props.uuid)

        return await self.session.scalar(query)

    async def find_many(self, props: ICompanyFindManyRepository) -> Sequence[Company]:
        query_filter: DictType = {}

        query: Select = (
            select(Company).where(**query_filter).offset(props.page).limit(props.limit)
        )

        return (await self.session.scalars(query)).all()
