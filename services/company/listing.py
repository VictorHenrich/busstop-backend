from typing import Optional, Sequence

from models import Company, database
from repositories.company import CompanyRepository, CompanyListingRepositoryProps
from utils.patterns import IService, IFindManyRepository, AbstractBaseEntity


class CompanyListingServiceProps(AbstractBaseEntity):
    company_name: Optional[str]


class CompanyListingService(IService[Sequence[Company]]):
    def __init__(self, company_name: Optional[str] = None) -> None:
        self.__props: CompanyListingServiceProps = CompanyListingServiceProps(
            company_name=company_name
        )

    async def execute(self) -> Sequence[Company]:
        async with database.create_async_session() as session:
            company_repository: IFindManyRepository[
                CompanyListingRepositoryProps, Company
            ] = CompanyRepository(session)

            return await company_repository.find_many(self.__props)
