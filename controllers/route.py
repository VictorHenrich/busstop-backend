from typing import Sequence, Optional, List

from server.instances import ServerInstances
from services.route import RouteService
from models import Route
from utils.responses import JSONBaseResponse, SuccessJSONResponse
from utils.entities import RouteBodyEntity, RouteEntity
from utils.constants import ROUTE_ENDPOINT_NAME
from utils.functions import handle_route_body, get_route_entity


@ServerInstances.api.get(f"{ROUTE_ENDPOINT_NAME}/{{company_uuid}}")
async def list_routes(company_uuid: str) -> JSONBaseResponse[List[RouteEntity]]:
    route_service: RouteService = RouteService()

    routes: Sequence[Route] = await route_service.find_routes(company_uuid=company_uuid)

    routes_handled: List[RouteEntity] = [get_route_entity(route) for route in routes]

    return SuccessJSONResponse(content=routes_handled)


@ServerInstances.api.get(f"{ROUTE_ENDPOINT_NAME}/{{route_uuid}}")
async def get_route(route_uuid: str) -> JSONBaseResponse[Optional[RouteEntity]]:
    route_service: RouteService = RouteService()

    route: Optional[Route] = await route_service.find_route(route_uuid)

    route_handled: Optional[RouteEntity] = handle_route_body(route)

    return SuccessJSONResponse(content=route_handled)


@ServerInstances.api.post(f"{ROUTE_ENDPOINT_NAME}/{{company_uuid}}")
async def create_route(
    company_uuid: str, body: RouteBodyEntity
) -> JSONBaseResponse[Optional[RouteEntity]]:
    route_service: RouteService = RouteService()

    route: Optional[Route] = await route_service.create_route(
        company_uuid=company_uuid,
        description=body.description,
        point_uuids=body.point_uuids,
    )

    route_handled: Optional[RouteEntity] = handle_route_body(route)

    return SuccessJSONResponse(content=route_handled)


@ServerInstances.api.put(f"{ROUTE_ENDPOINT_NAME}/{{route_uuid}}")
async def update_route(
    route_uuid: str, body: RouteBodyEntity
) -> JSONBaseResponse[Optional[RouteEntity]]:
    route_service: RouteService = RouteService()

    route: Optional[Route] = await route_service.update_route(
        route_uuid=route_uuid,
        description=body.description,
        point_uuids=body.point_uuids,
    )

    route_handled: Optional[RouteEntity] = handle_route_body(route)

    return SuccessJSONResponse(content=route_handled)


@ServerInstances.api.delete(f"{ROUTE_ENDPOINT_NAME}/{{route_uuid}}")
async def delete_route(route_uuid: str) -> JSONBaseResponse[Optional[RouteEntity]]:
    route_service: RouteService = RouteService()

    route: Optional[Route] = await route_service.delete_route(
        route_uuid=route_uuid,
    )

    route_handled: Optional[RouteEntity] = handle_route_body(route)

    return SuccessJSONResponse(content=route_handled)
