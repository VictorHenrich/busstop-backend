from typing import Sequence, Optional, List
from fastapi.routing import APIRouter

from server.instances import ServerInstances
from services.point import PointService
from models import Point
from utils.responses import JSONResponse
from utils.entities import PointEntity, PointBodyEntity
from utils.constants import POINT_ENPOINT_NAME
from utils.functions import handle_point_body


router: APIRouter = APIRouter(prefix=POINT_ENPOINT_NAME)


@router.get("/{{company_uuid}}")
async def list_points(
    company_uuid: str, uuids: List[str] = []
) -> JSONResponse[List[PointEntity]]:
    point_service: PointService = PointService()

    points: Sequence[Point] = await point_service.find_points(
        company_uuid=company_uuid, point_uuids=uuids
    )

    points_handled: List[PointEntity] = [
        PointEntity(
            uuid=point.uuid,
            address_state=point.address_state,
            address_city=point.address_city,
            address_neighborhood=point.address_neighborhood,
            address_street=point.address_street,
            address_number=point.address_number,
            latitude=point.latitude,
            longitude=point.longitude,
        )
        for point in points
    ]

    return JSONResponse(content=points_handled)


@router.get("/{{point_uuid}}")
async def get_point(point_uuid: str) -> JSONResponse[Optional[PointEntity]]:
    point_service: PointService = PointService()

    point: Optional[Point] = await point_service.find_point(point_uuid)

    point_handled: Optional[PointEntity] = handle_point_body(point)

    return JSONResponse(content=point_handled)


@router.post("/{{company_uuid}}")
async def create_point(
    company_uuid: str, point_body: PointBodyEntity
) -> JSONResponse[Optional[PointEntity]]:
    point_service: PointService = PointService()

    point: Optional[Point] = await point_service.create_point(
        company_uuid=company_uuid,
        address_state=point_body.address_state,
        address_city=point_body.address_city,
        address_neighborhood=point_body.address_neighborhood,
        address_street=point_body.address_street,
        address_number=point_body.address_number,
        latitude=point_body.latitude,
        longitude=point_body.longitude,
    )

    point_handled: Optional[PointEntity] = handle_point_body(point)

    return JSONResponse(content=point_handled)


@router.put("/{{point_uuid}}")
async def update_point(
    point_uuid: str, point_body: PointBodyEntity
) -> JSONResponse[Optional[PointEntity]]:
    point_service: PointService = PointService()

    point: Optional[Point] = await point_service.update_point(
        point_uuid=point_uuid,
        address_state=point_body.address_state,
        address_city=point_body.address_city,
        address_neighborhood=point_body.address_neighborhood,
        address_street=point_body.address_street,
        address_number=point_body.address_number,
        latitude=point_body.latitude,
        longitude=point_body.longitude,
    )

    point_handled: Optional[PointEntity] = handle_point_body(point)

    return JSONResponse(content=point_handled)


@router.delete("/{{point_uuid}}")
async def delete_point(point_uuid: str) -> JSONResponse[Optional[PointEntity]]:
    point_service: PointService = PointService()

    point: Optional[Point] = await point_service.delete_point(point_uuid)

    point_handled: Optional[PointEntity] = handle_point_body(point)

    return JSONResponse(content=point_handled)


ServerInstances.api.include_router(router)
