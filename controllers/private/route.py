from typing import Sequence, Optional, List
from fastapi.routing import APIRouter

from server.instances import ServerInstances
from services.route import RouteService
from models import Route
from utils.responses import JSONResponse
from utils.entities import RouteBodyEntity, RouteEntity
from utils.constants import ROUTE_ENDPOINT_NAME, SWAGGER_ROUTE_SESSION_TAG
from utils.functions import handle_route_body, get_route_entity


router: APIRouter = APIRouter(
    prefix=ROUTE_ENDPOINT_NAME, tags=[SWAGGER_ROUTE_SESSION_TAG]
)


@router.get("/{{company_uuid}}")
async def list_routes(company_uuid: str) -> JSONResponse[List[RouteEntity]]:
    route_service: RouteService = RouteService()

    routes: Sequence[Route] = await route_service.find_routes(company_uuid=company_uuid)

    routes_handled: List[RouteEntity] = [get_route_entity(route) for route in routes]

    return JSONResponse(content=routes_handled)


@router.get("/{{route_uuid}}")
async def get_route(route_uuid: str) -> JSONResponse[Optional[RouteEntity]]:
    route_service: RouteService = RouteService()

    route: Optional[Route] = await route_service.find_route(route_uuid)

    route_handled: Optional[RouteEntity] = handle_route_body(route)

    return JSONResponse(content=route_handled)


@router.post("/{{company_uuid}}")
async def create_route(
    company_uuid: str, body: RouteBodyEntity
) -> JSONResponse[Optional[RouteEntity]]:
    route_service: RouteService = RouteService()

    route: Optional[Route] = await route_service.create_route(
        company_uuid=company_uuid,
        description=body.description,
        point_uuids=body.point_uuids,
        closing_time=body.closing_time,
        opening_time=body.opening_time,
        ticket_price=body.ticket_price,
    )

    route_handled: Optional[RouteEntity] = handle_route_body(route)

    return JSONResponse(content=route_handled)


@router.put("/{{route_uuid}}")
async def update_route(
    route_uuid: str, body: RouteBodyEntity
) -> JSONResponse[Optional[RouteEntity]]:
    route_service: RouteService = RouteService()

    route: Optional[Route] = await route_service.update_route(
        route_uuid=route_uuid,
        description=body.description,
        closing_time=body.closing_time,
        opening_time=body.opening_time,
        point_uuids=body.point_uuids,
        ticket_price=body.ticket_price,
    )

    route_handled: Optional[RouteEntity] = handle_route_body(route)

    return JSONResponse(content=route_handled)


@router.delete("/{{route_uuid}}")
async def delete_route(route_uuid: str) -> JSONResponse[Optional[RouteEntity]]:
    route_service: RouteService = RouteService()

    route: Optional[Route] = await route_service.delete_route(
        route_uuid=route_uuid,
    )

    route_handled: Optional[RouteEntity] = handle_route_body(route)

    return JSONResponse(content=route_handled)


ServerInstances.api.include_router(router)
