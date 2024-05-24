from pydantic import BaseModel

from server.instances import ServerInstances
from server.database import Database
from repositories.company import CompanyRepository, CompanyCreationRepositoryProps
from utils.patterns import IService, ICreateRepository
from utils.constants import DATABASE_INSTANCE_NAME


class CompanyCreationServiceProps(BaseModel):
    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class CompanyCreationService(IService[CompanyCreationServiceProps, None]):
    def __init__(self, props: CompanyCreationServiceProps) -> None:
        self.__company: CompanyCreationServiceProps = props

    async def execute(self) -> None:
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            company_repository: ICreateRepository[
                CompanyCreationRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.create(self.__company)
