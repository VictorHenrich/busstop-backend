from typing import Sequence
from fastapi.routing import APIRouter

from server.instances import ServerInstances
from services.geo import GeoService
from models import Point
from utils.responses import JSONSuccessResponse
from utils.entities import PointBodyEntity
from utils.constants import GEO_ENPOINT_NAME, SWAGGER_GEO_SESSION_TAG


router: APIRouter = APIRouter(prefix=GEO_ENPOINT_NAME, tags=[SWAGGER_GEO_SESSION_TAG])


@router.get("/find")
async def find_address(
    address_description: str,
) -> JSONSuccessResponse[Sequence[PointBodyEntity]]:
    geo_service: GeoService = GeoService()

    points: Sequence[Point] = await geo_service.find_address(address_description)

    data: Sequence[PointBodyEntity] = [
        PointBodyEntity(
            address_zip_code=point.address_zip_code,
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

    return JSONSuccessResponse(content=data)


ServerInstances.api.include_router(router)
