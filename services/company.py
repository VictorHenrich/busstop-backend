from typing import Optional, Sequence
from copy import copy

from models import Company, database
from repositories.company import (
    CompanyRepository,
    CompanyListingRepositoryProps,
    CompanyCaptureRepositoryProps,
    CompanyExclusionRepositoryProps,
    CompanyUpdateRepositoryProps,
    CompanyCreationRepositoryProps,
)
from utils.patterns import (
    AbstractBaseEntity,
    ICreateRepository,
    IDeleteRepository,
    IFindManyRepository,
    IFindRepository,
    IUpdateRepository,
)
from utils.exceptions import ModelNotFound


class CompanyListingProps(AbstractBaseEntity):
    company_name: Optional[str]

    limit: int

    page: int


class CompanyUpdateProps(AbstractBaseEntity):
    uuid: str

    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class CompanyCaptureProps(AbstractBaseEntity):
    uuid: str


class CompanyExclusionProps(AbstractBaseEntity):
    uuid: str


class CompanyCreationProps(AbstractBaseEntity):
    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class CompanyService:
    async def find_companies(
        self, company_name: Optional[str] = None, limit: int = 50, page: int = 0
    ) -> Sequence[Company]:
        async with database.create_async_session() as session:
            company_repository: IFindManyRepository[
                CompanyListingRepositoryProps, Company
            ] = CompanyRepository(session)

            props: CompanyListingRepositoryProps = CompanyListingProps(
                company_name=company_name, limit=limit, page=page
            )

            return await company_repository.find_many(props)

    async def find_company(self, company_uuid: str) -> Company:
        async with database.create_async_session() as session:
            company_repository: IFindRepository[
                CompanyCaptureRepositoryProps, Company
            ] = CompanyRepository(session)

            company_props: CompanyCaptureRepositoryProps = CompanyCaptureProps(
                uuid=company_uuid
            )

            company: Optional[Company] = await company_repository.find(company_props)

            if not company:
                raise ModelNotFound(Company, company_uuid)

            return company

    async def delete_company(self, company_uuid: str) -> Optional[Company]:
        async with database.create_async_session() as session:
            company_repository: IDeleteRepository[
                CompanyExclusionRepositoryProps, Optional[Company]
            ] = CompanyRepository(session)

            props: CompanyExclusionRepositoryProps = CompanyExclusionProps(
                uuid=company_uuid
            )

            company: Optional[Company] = await company_repository.delete(props)

            if company is not None:
                return copy(company)

            await session.commit()

    async def update_company(
        self,
        company_uuid: str,
        company_name: str,
        fantasy_name: str,
        document_cnpj: str,
        email: str,
    ) -> Optional[Company]:
        async with database.create_async_session() as session:
            company_repository: IUpdateRepository[
                CompanyUpdateRepositoryProps, Optional[Company]
            ] = CompanyRepository(session)

            company_props: CompanyUpdateRepositoryProps = CompanyUpdateProps(
                uuid=company_uuid,
                company_name=company_name,
                fantasy_name=fantasy_name,
                document_cnpj=document_cnpj,
                email=email,
            )

            company: Optional[Company] = await company_repository.update(company_props)

            await session.commit()

            return company

    async def create_company(
        self, company_name: str, fantasy_name: str, document_cnpj: str, email: str
    ) -> Optional[Company]:
        async with database.create_async_session() as session:
            company_repository: ICreateRepository[
                CompanyCreationRepositoryProps, Optional[Company]
            ] = CompanyRepository(session)

            company_data: CompanyCreationRepositoryProps = CompanyCreationProps(
                company_name=company_name,
                fantasy_name=fantasy_name,
                document_cnpj=document_cnpj,
                email=email,
            )

            company: Optional[Company] = await company_repository.create(company_data)

            await session.commit()

            return company
