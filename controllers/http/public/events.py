from fastapi.routing import APIRouter

from server.instances import ServerInstances
from services.vehicle_events import VehicleEventsService
from utils.responses import JSONSuccessResponse
from utils.constants import (
    EVENTS_ENDPOINT_NAME,
    VEHICLE_ENDPOINT_NAME,
    SWAGGER_EVENTS_SESSION_TAG,
)
from utils.entities import VehiclePositionBodyEntity


router: APIRouter = APIRouter(
    prefix=EVENTS_ENDPOINT_NAME, tags=[SWAGGER_EVENTS_SESSION_TAG]
)


@router.post(f"{VEHICLE_ENDPOINT_NAME}/{{vehicle_uuid}}/position")
async def capture_vehicle_position(
    body: VehiclePositionBodyEntity, vehicle_uuid: str
) -> JSONSuccessResponse:
    vehicle_events_service: VehicleEventsService = VehicleEventsService()

    await vehicle_events_service.process_vehicle_position(
        vehicle_uuid=vehicle_uuid, latitude=body.latitude, longitude=body.longitude
    )

    return JSONSuccessResponse()


ServerInstances.general_api.include_router(router)
