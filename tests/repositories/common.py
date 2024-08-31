from typing import Sequence
from unittest import IsolatedAsyncioTestCase
from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import time
import asyncio

from models import Agent, Company, Point, Route, User, Vehicle, database
from utils.types import VehicleType


class AsyncBaseRepositoryOnlineTestCase(IsolatedAsyncioTestCase, ABC):
    @property
    def company(self) -> Company:
        return self.__company

    @property
    def point(self) -> Point:
        return self.__point

    @property
    def agent(self) -> Agent:
        return self.__agent

    @property
    def route(self) -> Route:
        return self.__route

    @property
    def vehicle(self) -> Vehicle:
        return self.__vehicle

    @property
    def user(self) -> User:
        return self.__user

    async def asyncSetUp(self) -> None:
        await self.create_setup()

    async def create_setup(self) -> None:
        async with database.create_async_session() as session:
            self.__company, self.__user = await asyncio.gather(
                self.create_company(session), self.create_user(session)
            )

            await asyncio.gather(
                session.refresh(self.__company), session.refresh(self.__user)
            )

            self.__agent, self.__point, self.__vehicle = await asyncio.gather(
                self.create_agent(session, self.__company),
                self.create_point(session, self.__company),
                self.create_vehicle(session, self.__company),
            )

            await asyncio.gather(
                session.refresh(self.__agent),
                session.refresh(self.__point),
                session.refresh(self.__vehicle),
            )

            (self.__route,) = await asyncio.gather(
                self.create_route(session, self.__company, (self.__point,))
            )

            await asyncio.gather(session.refresh(self.__route))

            await session.commit()

    async def create_agent(
        self,
        session: AsyncSession,
        company: Company,
        name: str = "usuario_teste",
        email: str = "usuario_teste@exemplo.com",
        password: str = "1234",
    ) -> Agent:
        agent: Agent = Agent(company=company, name=name, email=email, password=password)

        session.add(agent)

        return agent

    async def create_company(
        self,
        session: AsyncSession,
        company_name: str = "Empresa Teste",
        fantasy_name: str = "Teste",
        document_cnpj: str = "u000000000000000",
        email: str = "empresa_teste@exemplo.com",
    ) -> Company:
        company: Company = Company(
            company_name=company_name,
            fantasy_name=fantasy_name,
            document_cnpj=document_cnpj,
            email=email,
        )

        session.add(company)

        return company

    async def create_point(
        self,
        session: AsyncSession,
        company: Company,
        address_zip_code: str = "Teste",
        address_state: str = "u000000000000000",
        address_city: str = "empresa_teste@exemplo.com",
        address_neighborhood: str = "Empresa Teste",
        address_street: str = "Teste",
        address_number: str = "u000000000000000",
        latitude: str = "empresa_teste@exemplo.com",
        longitude: str = "Empresa Teste",
        place_id: str = "Teste",
    ) -> Point:
        point: Point = Point(
            company=company,
            address_zip_code=address_zip_code,
            address_state=address_state,
            address_city=address_city,
            address_neighborhood=address_neighborhood,
            address_street=address_street,
            address_number=address_number,
            latitude=latitude,
            longitude=longitude,
            place_id=place_id,
        )

        session.add(point)

        return point

    async def create_route(
        self,
        session: AsyncSession,
        company: Company,
        points: Sequence[Point],
        description: str = "Rota teste",
        opening_time: time = time(),
        closing_time: time = time(),
        ticket_price: float = 0,
    ) -> Route:
        route: Route = Route(
            company=company,
            points=points,
            description=description,
            opening_time=opening_time,
            closing_time=closing_time,
            ticket_price=ticket_price,
        )

        session.add(route)

        return route

    async def create_vehicle(
        self,
        session: AsyncSession,
        company: Company,
        type: VehicleType = VehicleType.BUS,
        plate: str = "AAk123",
    ) -> Vehicle:
        vehicle: Vehicle = Vehicle(company=company, type=type.value, plate=plate)

        session.add(vehicle)

        return vehicle

    async def create_user(
        self,
        session: AsyncSession,
        name: str = "usuario_teste",
        email: str = "usuario_teste@exemplo.com",
        password: str = "1234",
    ) -> User:
        user: User = User(name=name, email=email, password=password)

        session.add(user)

        return user
