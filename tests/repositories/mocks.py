from datetime import time

from models import Company, Agent, Point, Route, Vehicle, database


async def create_company(
    company_name: str = "Empresa Teste",
    fantasy_name: str = "Nome Fantasia Teste",
    document_cnpj: str = "000000000",
    email: str = "teste@email.com",
) -> Company:
    async with database.create_async_session() as session:
        company: Company = Company(
            company_name=company_name,
            fantasy_name=fantasy_name,
            document_cnpj=document_cnpj,
            email=email,
        )

        session.add(company)

        await session.commit()

        await session.refresh(company)

        return company


async def create_agent(
    company: Company,
    name: str = "teste",
    email: str = "usuario_teste@email.com",
    password: str = "1234",
) -> Agent:
    async with database.create_async_session() as session:
        agent: Agent = Agent(name=name, email=email, password=password, company=company)

        session.add(agent)

        await session.commit()

        await session.refresh(agent)

        return agent


async def create_point(
    company: Company,
    address_zip_code: str = "00000",
    address_state: str = "SC",
    address_city: str = "Cidade teste",
    address_neighborhood: str = "Bairro teste",
    address_street: str = "Rua teste",
    address_number: str = "00",
    latitude: str = "0",
    longitude: str = "0",
    place_id: str = "1234",
) -> Point:
    async with database.create_async_session() as session:
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

        await session.commit()

        await session.refresh(point)

        return point


async def create_route(
    company: Company,
    description: str = "Rota para centro",
    opening_time: time = time(),
    closing_time: time = time(),
    ticker_price: float = 0,
) -> Route:
    async with database.create_async_session() as session:
        route: Route = Route(
            company=company,
            description=description,
            opening_time=opening_time,
            closing_time=closing_time,
            ticker_price=ticker_price,
        )

        session.add(route)

        await session.commit()

        await session.refresh(route)

        return route


async def create_vehicle(
    company: Company,
    type: str = "",
    plate: str = "1234",
) -> Vehicle:
    async with database.create_async_session() as session:
        vehicle: Vehicle = Vehicle()

        session.add(vehicle)

        await session.commit()

        await session.refresh(vehicle)

        return vehicle
