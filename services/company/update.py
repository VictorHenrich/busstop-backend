from pydantic import BaseModel

from server.instances import ServerInstances
from server.database import Database
from repositories.company import CompanyRepository, CompanyUpdateRepositoryProps
from utils.patterns import IService, IUpdateRepository
from utils.constants import DATABASE_INSTANCE_NAME


class CompanyUpdateServiceProps(BaseModel):
    uuid: str

    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class CompanyUpdateService(IService[CompanyUpdateServiceProps, None]):
    def __init__(self, props: CompanyUpdateServiceProps) -> None:
        self.__props: CompanyUpdateServiceProps = props

    async def execute(self) -> None:
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            company_repository: IUpdateRepository[
                CompanyUpdateRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.update(self.__props)
