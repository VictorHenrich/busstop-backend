from typing import Sequence, Optional, List

from server.instances import ServerInstances
from services.point.creation import PointCreationService
from services.point.update import PointUpdateService
from services.point.exclusion import PointExclusionService
from services.point.capture import PointCaptureService
from services.point.listing import PointListingService
from models import Point
from utils.responses import JSONBaseResponse, SuccessJSONResponse
from utils.patterns import IService
from utils.entities import PointEntity, PointBodyEntity
from utils.constants import POINT_ENPOINT_NAME


@ServerInstances.api.get(f"{POINT_ENPOINT_NAME}/{{company_uuid}}")
async def list_points(
    company_uuid: str, uuids: List[str] = []
) -> JSONBaseResponse[List[PointEntity]]:
    point_listing_service: IService[Sequence[Point]] = PointListingService(
        company_uuid=company_uuid, uuids=uuids
    )

    points: Sequence[Point] = await point_listing_service.execute()

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

    return SuccessJSONResponse(content=points_handled)


@ServerInstances.api.get(f"{POINT_ENPOINT_NAME}/{{point_uuid}}")
async def get_point(point_uuid: str) -> JSONBaseResponse:
    point_capture_service: IService[Optional[Point]] = PointCaptureService(point_uuid)

    point: Optional[Point] = await point_capture_service.execute()

    point_handled: Optional[PointEntity] = None

    if point:
        point_handled = PointEntity(
            uuid=point.uuid,
            address_state=point.address_state,
            address_city=point.address_city,
            address_neighborhood=point.address_neighborhood,
            address_street=point.address_street,
            address_number=point.address_number,
            latitude=point.latitude,
            longitude=point.longitude,
        )

    return SuccessJSONResponse(content=point_handled)


@ServerInstances.api.post(f"{POINT_ENPOINT_NAME}/{{company_uuid}}")
async def create_point(
    company_uuid: str, point_body: PointBodyEntity
) -> JSONBaseResponse[Optional[PointEntity]]:
    point_creation_service: IService[Optional[Point]] = PointCreationService(
        company_uuid=company_uuid,
        address_state=point_body.address_state,
        address_city=point_body.address_city,
        address_neighborhood=point_body.address_neighborhood,
        address_street=point_body.address_street,
        address_number=point_body.address_number,
        latitude=point_body.latitude,
        longitude=point_body.longitude,
    )

    point: Optional[Point] = await point_creation_service.execute()

    point_handled: Optional[PointEntity] = None

    if point:
        point_handled = PointEntity(
            uuid=point.uuid,
            address_state=point.address_state,
            address_city=point.address_city,
            address_neighborhood=point.address_neighborhood,
            address_street=point.address_street,
            address_number=point.address_number,
            latitude=point.latitude,
            longitude=point.longitude,
        )

    return SuccessJSONResponse(content=point_handled)


@ServerInstances.api.put(f"{POINT_ENPOINT_NAME}/{{point_uuid}}")
async def update_point(
    point_uuid: str, point_body: PointBodyEntity
) -> JSONBaseResponse[Optional[PointEntity]]:
    point_update_service: IService[Optional[Point]] = PointUpdateService(
        point_uuid=point_uuid,
        address_state=point_body.address_state,
        address_city=point_body.address_city,
        address_neighborhood=point_body.address_neighborhood,
        address_street=point_body.address_street,
        address_number=point_body.address_number,
        latitude=point_body.latitude,
        longitude=point_body.longitude,
    )

    point: Optional[Point] = await point_update_service.execute()

    point_handled: Optional[PointEntity] = None

    if point:
        point_handled = PointEntity(
            uuid=point.uuid,
            address_state=point.address_state,
            address_city=point.address_city,
            address_neighborhood=point.address_neighborhood,
            address_street=point.address_street,
            address_number=point.address_number,
            latitude=point.latitude,
            longitude=point.longitude,
        )

    return SuccessJSONResponse(content=point_handled)


@ServerInstances.api.delete(f"{POINT_ENPOINT_NAME}/{{point_uuid}}")
async def delete_point(point_uuid: str) -> JSONBaseResponse[Optional[PointEntity]]:
    point_exclusion_service: IService[Optional[Point]] = PointExclusionService(
        point_uuid
    )

    point: Optional[Point] = await point_exclusion_service.execute()

    point_handled: Optional[PointEntity] = None

    if point:
        point_handled = PointEntity(
            uuid=point.uuid,
            address_state=point.address_state,
            address_city=point.address_city,
            address_neighborhood=point.address_neighborhood,
            address_street=point.address_street,
            address_number=point.address_number,
            latitude=point.latitude,
            longitude=point.longitude,
        )

    return SuccessJSONResponse(content=point_handled)
