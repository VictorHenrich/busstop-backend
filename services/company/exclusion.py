from pydantic import BaseModel

from server.instances import ServerInstances
from server.database import Database
from repositories.company import CompanyRepository, CompanyExclusionRepositoryProps
from utils.patterns import IService, IDeleteRepository
from utils.constants import DATABASE_INSTANCE_NAME


class CompanyExclusionServiceProps(BaseModel):
    uuid: str


class CompanyExclusionService(IService[CompanyExclusionServiceProps, None]):
    def __init__(self, props: CompanyExclusionServiceProps) -> None:
        self.__props: CompanyExclusionServiceProps = props

    async def execute(self) -> None:
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            company_repository: IDeleteRepository[
                CompanyExclusionRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.delete(self.__props)

            await session.commit()
