from typing import Optional, Sequence
from copy import copy

from models import Company, database
from repositories.company import (
    CompanyRepository,
    ICompanyFindManyRepository,
    ICompanyFindRepository,
    ICompanyDeleteRepository,
    ICompanyUpdateRepository,
    ICompanyCreateRepository,
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

    instance: Optional[Company]


class CompanyCaptureProps(AbstractBaseEntity):
    uuid: str


class CompanyExclusionProps(AbstractBaseEntity):
    uuid: str
    instance: Optional[Company]


class CompanyCreationProps(AbstractBaseEntity):
    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class CompanyService:
    async def __find_company_by_id(
        self, company_uuid: str, company_repository: CompanyRepository
    ) -> Company:
        company_props: ICompanyFindRepository = CompanyCaptureProps(uuid=company_uuid)

        company: Optional[Company] = await company_repository.find(company_props)

        if not company:
            raise ModelNotFound(Company, company_uuid)

        return company

    async def find_companies(
        self, company_name: Optional[str] = None, limit: int = 50, page: int = 0
    ) -> Sequence[Company]:
        async with database.create_async_session() as session:
            company_repository: IFindManyRepository[
                ICompanyFindManyRepository, Company
            ] = CompanyRepository(session)

            props: ICompanyFindManyRepository = CompanyListingProps(
                company_name=company_name, limit=limit, page=page
            )

            return await company_repository.find_many(props)

    async def find_company(self, company_uuid: str) -> Company:
        async with database.create_async_session() as session:
            company_repository: IFindRepository[ICompanyFindRepository, Company] = (
                CompanyRepository(session)
            )

            return await self.__find_company_by_id(company_uuid, company_repository)

    async def delete_company(self, company_uuid: str) -> Optional[Company]:
        async with database.create_async_session() as session:
            company_repository: IDeleteRepository[
                ICompanyDeleteRepository, Optional[Company]
            ] = CompanyRepository(session)

            company: Company = await self.__find_company_by_id(
                company_uuid, company_repository
            )

            props: ICompanyDeleteRepository = CompanyExclusionProps(
                uuid=company_uuid, instance=company
            )

            await company_repository.delete(props)

            await session.commit()

            return copy(company)

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
                ICompanyUpdateRepository, Optional[Company]
            ] = CompanyRepository(session)

            company: Company = await self.__find_company_by_id(
                company_uuid, company_repository
            )

            company_props: ICompanyUpdateRepository = CompanyUpdateProps(
                instance=company,
                uuid=company.uuid,
                company_name=company_name,
                fantasy_name=fantasy_name,
                document_cnpj=document_cnpj,
                email=email,
            )

            await company_repository.update(company_props)

            await session.commit()

            await session.refresh(company)

            return company

    async def create_company(
        self, company_name: str, fantasy_name: str, document_cnpj: str, email: str
    ) -> Optional[Company]:
        async with database.create_async_session() as session:
            company_repository: ICreateRepository[
                ICompanyCreateRepository, Optional[Company]
            ] = CompanyRepository(session)

            company_data: ICompanyCreateRepository = CompanyCreationProps(
                company_name=company_name,
                fantasy_name=fantasy_name,
                document_cnpj=document_cnpj,
                email=email,
            )

            company: Optional[Company] = await company_repository.create(company_data)

            return company
