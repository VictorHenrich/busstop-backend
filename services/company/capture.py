from typing import Optional

from server.instances import ServerInstances
from server.database import Database
from models.company import Company
from repositories.company import CompanyRepository, CompanyCaptureRepositoryProps
from utils.patterns import IService, IFindRepository, AbstractBaseEntity
from utils.constants import DATABASE_INSTANCE_NAME
from utils.exceptions import ModelNotFound


class CompanyCaptureProps(AbstractBaseEntity):
    uuid: str


class CompanyCaptureService(IService[Company]):
    def __init__(self, company_uuid: str) -> None:
        self.__company_uuid: str = company_uuid

    async def execute(self) -> Company:
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            company_repository: IFindRepository[
                CompanyCaptureRepositoryProps, Company
            ] = CompanyRepository(session)

            company_props: CompanyCaptureRepositoryProps = CompanyCaptureProps(
                uuid=self.__company_uuid
            )

            company: Optional[Company] = await company_repository.find(company_props)

            if not company:
                raise ModelNotFound(Company, self.__company_uuid)

            return company
