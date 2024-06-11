from typing import Sequence, Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, AsyncMock


from models import Company
from repositories.company import (
    CompanyRepository,
    CompanyCreationRepositoryProps,
    CompanyUpdateRepositoryProps,
    CompanyExclusionRepositoryProps,
    CompanyCaptureRepositoryProps,
    CompanyListingRepositoryProps,
)
from utils.patterns import (
    ICreateRepository,
    IFindRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindManyRepository,
)


class CompanyRepositoryTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_company: Mock = Mock()

        self.__mock_session: AsyncMock = AsyncMock()

        self.__mock_company.company_name = "Empresa teste alterado"
        self.__mock_company.fantasy_name = "Nome fantasia alterado"
        self.__mock_company.document_cnpj = "02988790000"
        self.__mock_company.email = "victorhenrich993@gmail.com"
        self.__mock_company.uuid = "6df97b7d-2beb-4d60-ae75-b742ac3df68a"

    async def test_create(self) -> None:
        self.__mock_session.scalar.return_value = self.__mock_company

        company_repository: ICreateRepository[
            CompanyCreationRepositoryProps, Optional[Company]
        ] = CompanyRepository(self.__mock_session)

        company: Optional[Company] = await company_repository.create(
            self.__mock_company
        )

        self.assertIsNotNone(company)
        self.assertEqual(company, self.__mock_company)

    async def test_update(self) -> None:
        self.__mock_session.scalar.return_value = self.__mock_company

        company_repository: IUpdateRepository[
            CompanyUpdateRepositoryProps, Optional[Company]
        ] = CompanyRepository(self.__mock_session)

        company: Optional[Company] = await company_repository.update(
            self.__mock_company
        )

        self.assertIsNotNone(company)
        self.assertEqual(company, self.__mock_company)

    async def test_delete(self) -> None:
        self.__mock_session.scalar.return_value = self.__mock_company

        filter_props: Mock = Mock(uuid="")

        company_repository: IDeleteRepository[
            CompanyExclusionRepositoryProps, Optional[Company]
        ] = CompanyRepository(self.__mock_session)

        company: Optional[Company] = await company_repository.delete(filter_props)

        self.assertIsNotNone(company)
        self.assertEqual(company, self.__mock_company)

    async def test_get(self) -> None:
        self.__mock_session.scalar.return_value = self.__mock_company

        filter_props: Mock = Mock(uuid="")

        company_repository: IFindRepository[
            CompanyCaptureRepositoryProps, Company
        ] = CompanyRepository(self.__mock_session)

        company: Optional[Company] = await company_repository.find(filter_props)

        self.assertIsNotNone(company)
        self.assertEqual(company, self.__mock_company)

    async def test_list(self) -> None:
        filter_props: Mock = Mock(company_name="TESTE", limit=50, page=0)

        mock_result_session: Mock = Mock()

        mock_result_session.all.return_value = [self.__mock_company]

        self.__mock_session.scalars.return_value = mock_result_session

        company_repository: IFindManyRepository[
            CompanyListingRepositoryProps, Company
        ] = CompanyRepository(self.__mock_session)

        companies: Sequence[Company] = await company_repository.find_many(filter_props)

        self.assertNotEqual(companies, [])
        self.assertListEqual(list(companies), [self.__mock_company])
