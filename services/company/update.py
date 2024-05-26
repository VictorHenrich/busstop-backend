from models import database
from repositories.company import CompanyRepository, CompanyUpdateRepositoryProps
from utils.patterns import IService, IUpdateRepository, AbstractBaseEntity


class CompanyUpdateServiceProps(AbstractBaseEntity):
    uuid: str

    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class CompanyUpdateService(IService[None]):
    def __init__(
        self,
        uuid: str,
        company_name: str,
        fantasy_name: str,
        document_cnpj: str,
        email: str,
    ) -> None:
        self.__props: CompanyUpdateServiceProps = CompanyUpdateServiceProps(
            uuid=uuid,
            company_name=company_name,
            fantasy_name=fantasy_name,
            document_cnpj=document_cnpj,
            email=email,
        )

    async def execute(self) -> None:
        async with database.create_async_session() as session:
            company_repository: IUpdateRepository[
                CompanyUpdateRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.update(self.__props)

            await session.commit()
