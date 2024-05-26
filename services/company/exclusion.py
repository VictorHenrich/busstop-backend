from dataclasses import dataclass

from server.instances import ServerInstances
from server.database import Database
from repositories.company import CompanyRepository, CompanyExclusionRepositoryProps
from utils.patterns import IService, IDeleteRepository
from utils.constants import DATABASE_INSTANCE_NAME


@dataclass
class CompanyExclusionServiceProps:
    uuid: str


class CompanyExclusionService(IService[None]):
    def __init__(self, uuid: str) -> None:
        self.__props: CompanyExclusionServiceProps = CompanyExclusionServiceProps(
            uuid=uuid
        )

    async def execute(self) -> None:
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            company_repository: IDeleteRepository[
                CompanyExclusionRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.delete(self.__props)

            await session.commit()
