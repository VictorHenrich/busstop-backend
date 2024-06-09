from typing import Optional, List

from models import Point, Route, Company, Agent
from utils.entities import (
    PointEntity,
    RouteEntity,
    CompanyEntity,
    AgentEntity,
    AuthResultEntity,
)


def get_agent_entity(agent: Agent) -> AgentEntity:
    return AgentEntity(
        uuid=agent.uuid, email=agent.email, password=agent.password, name=agent.name
    )


def get_point_entity(point: Point) -> PointEntity:
    return PointEntity(
        uuid=point.uuid,
        address_state=point.address_state,
        address_city=point.address_city,
        address_neighborhood=point.address_neighborhood,
        address_street=point.address_street,
        address_number=point.address_number,
        latitude=point.latitude,
        longitude=point.longitude,
    )


def get_route_entity(route: Route) -> RouteEntity:
    points: List[PointEntity] = [get_point_entity(point) for point in route.points]

    return RouteEntity(uuid=route.uuid, description=route.description, points=points)


def get_company_entity(company: Company) -> CompanyEntity:
    return CompanyEntity(
        uuid=company.uuid,
        company_name=company.company_name,
        fantasy_name=company.fantasy_name,
        document_cnpj=company.document_cnpj,
        email=company.email,
    )


def handle_point_body(point: Optional[Point]) -> Optional[PointEntity]:
    if point:
        return get_point_entity(point)


def handle_route_body(route: Optional[Route]) -> Optional[RouteEntity]:
    if route is not None:
        return get_route_entity(route)


def handle_company_body(company: Optional[Company]) -> Optional[CompanyEntity]:
    if company is not None:
        return get_company_entity(company)


def handle_agent_body(agent: Optional[Agent]) -> Optional[AgentEntity]:
    if agent is not None:
        return get_agent_entity(agent)
