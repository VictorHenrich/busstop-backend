from typing import (
    Any,
    Callable,
    Awaitable,
    Mapping,
    Optional,
    List,
    AsyncGenerator,
    Union,
)
from fastapi import Request, Response
from fastapi.responses import JSONResponse

from models import Point, Route, Company, Agent
from utils.entities import (
    PointEntity,
    RouteEntity,
    CompanyEntity,
    AgentEntity,
)
from utils.constants import PUBLIC_ROUTES
from utils.responses import JSONErrorResponse


def get_agent_entity(agent: Agent) -> AgentEntity:
    return AgentEntity(
        uuid=agent.uuid, email=agent.email, password=agent.password, name=agent.name
    )


def get_point_entity(point: Point) -> PointEntity:
    return PointEntity(
        uuid=point.uuid,
        address_zip_code=point.address_zip_code,
        address_state=point.address_state,
        address_city=point.address_city,
        address_neighborhood=point.address_neighborhood,
        address_street=point.address_street,
        address_number=point.address_number,
        latitude=point.latitude,
        longitude=point.longitude,
    )


def get_route_entity(route: Route) -> RouteEntity:
    points: List[PointEntity] = [
        get_point_entity(route_point.point) for route_point in route.points
    ]

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


async def handle_call_errors(
    call_next: Callable[[Request], Awaitable[Response]], *args: Any
) -> Response:
    try:
        return await call_next(*args)

    except Exception as error:
        response: Mapping[str, Any] = JSONErrorResponse(reason=str(error)).model_dump()

        return JSONResponse(status_code=500, content=response)


async def validate_middleware_request(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> AsyncGenerator[Union[bool, Response], None]:
    validated: bool = bool([True for path in PUBLIC_ROUTES if path in request.url.path])

    yield validated

    if validated:
        yield await handle_call_errors(call_next, request)
