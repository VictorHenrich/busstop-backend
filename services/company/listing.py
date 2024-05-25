from typing import Optional, Sequence
from pydantic import BaseModel

from server.instances import ServerInstances
from server.database import Database
from models.company import Company
from repositories.company import CompanyRepository, CompanyListingRepositoryProps
from utils.patterns import IService, IFindManyRepository
from utils.constants import DATABASE_INSTANCE_NAME


class CompanyListingServiceProps(BaseModel):
    company_name: Optional[str]


class CompanyListingService(IService[Sequence[Company]]):
    def __init__(self, company_name: Optional[str] = None) -> None:
        self.__props: CompanyListingServiceProps = CompanyListingServiceProps(
            company_name=company_name
        )

    async def execute(self) -> Sequence[Company]:
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            company_repository: IFindManyRepository[
                CompanyListingRepositoryProps, Company
            ] = CompanyRepository(session)

            return await company_repository.find_many(self.__props)
