from dataclasses import dataclass

from server.instances import ServerInstances
from server.database import Database
from repositories.company import CompanyRepository, CompanyCreationRepositoryProps
from utils.patterns import IService, ICreateRepository
from utils.constants import DATABASE_INSTANCE_NAME


@dataclass
class CompanyCreationServiceProps:
    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class CompanyCreationService(IService[None]):
    def __init__(
        self, company_name: str, fantasy_name: str, document_cnpj: str, email: str
    ) -> None:
        self.__company_data: CompanyCreationServiceProps = CompanyCreationServiceProps(
            company_name=company_name,
            fantasy_name=fantasy_name,
            document_cnpj=document_cnpj,
            email=email,
        )

    async def execute(self) -> None:
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            company_repository: ICreateRepository[
                CompanyCreationRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.create(self.__company_data)

            await session.commit()
