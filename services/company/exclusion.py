from models import database
from repositories.company import CompanyRepository, CompanyExclusionRepositoryProps
from utils.patterns import IService, IDeleteRepository, AbstractBaseEntity


class CompanyExclusionServiceProps(AbstractBaseEntity):
    uuid: str


class CompanyExclusionService(IService[None]):
    def __init__(self, uuid: str) -> None:
        self.__props: CompanyExclusionServiceProps = CompanyExclusionServiceProps(
            uuid=uuid
        )

    async def execute(self) -> None:
        async with database.create_async_session() as session:
            company_repository: IDeleteRepository[
                CompanyExclusionRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.delete(self.__props)

            await session.commit()
