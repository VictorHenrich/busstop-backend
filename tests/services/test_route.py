from typing import Optional, Sequence
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, patch

from services.route import RouteService
from models import Company, Route, Point


class RouteServiceTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_async_session: AsyncMock = AsyncMock()

        self.__mock_async_session.__aenter__.side_effect = (
            lambda: self.__mock_async_session
        )

        self.__mock_async_session.commit.return_value = None

        self.__mock_points: Sequence[Point] = []

        self.__mock_route: Mock = Mock(
            description="",
            uuid="4932d9e1-c715-4b97-890a-ab2f678d3d11",
            instance=None,
            spec=Route,
        )

        self.__mock_company: Mock = Mock(
            company_name="Empresa Teste",
            fantasy_name="Nome Fantasia TESTE",
            document_cnpj="00000000",
            email="teste@gmail.com",
            uuid="6df97b7d-2beb-4d60-ae75-b742ac3df68a",
            spec=Company,
        )

    async def test_create(self) -> None:
        pass
