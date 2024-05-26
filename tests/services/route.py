from typing import Optional, Sequence
from unittest import TestCase
import logging
import asyncio


from utils.patterns import IService
from services.route.creation import RouteCreationService
from services.route.update import RouteUpdateService
from services.route.exclusion import RouteExclusionService
from services.route.capture import RouteCaptureService
from services.route.listing import RouteListingService
from models import Route


class RouteServiceCase(TestCase):
    def test_creation(self) -> None:
        async def main() -> None:
            point_creation_service: IService = RouteCreationService(
                company_uuid="f309cbfa-472d-4b29-8cc4-5da7704823d9",
                description="Rota de teste",
                point_uuids=[],
            )

            route: Optional[Route] = await point_creation_service.execute()

            logging.info(f"Route Created: {route}")

        asyncio.run(main())

    def test_update(self) -> None:
        async def main() -> None:
            point_update_service: IService = RouteUpdateService(
                route_uuid="68fa075f-074f-44d2-9160-f59aad4abcbf",
                description="Rota de teste alterada",
                point_uuids=[],
            )

            route: Optional[Route] = await point_update_service.execute()

            logging.info(f"Route Updated: {route}")

        asyncio.run(main())

    def test_exclusion(self) -> None:
        async def main() -> None:
            point_exclusion_service: IService = RouteExclusionService(
                route_uuid="ffca0064-04d3-4da3-8332-885ac82b1ab2",
            )

            route: Optional[Route] = await point_exclusion_service.execute()

            logging.info(f"Route Deleted: {route}")

        asyncio.run(main())

    def test_listing(self) -> None:
        async def main() -> None:
            point_listing_service: IService = RouteListingService(
                company_uuid="f309cbfa-472d-4b29-8cc4-5da7704823d9",
            )

            points: Sequence[Route] = await point_listing_service.execute()

            logging.info(f"Routes: {points}")

            self.assertNotEqual(points, [])

        asyncio.run(main())

    def test_capture(self) -> None:
        async def main() -> None:
            point_capture_service: IService = RouteCaptureService(
                route_uuid="68fa075f-074f-44d2-9160-f59aad4abcbf",
            )

            route: Optional[Route] = await point_capture_service.execute()

            logging.info(f"Route Captured: {route}")

            self.assertNotEqual(route, None)

        asyncio.run(main())
