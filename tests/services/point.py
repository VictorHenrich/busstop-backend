from typing import Optional, Sequence
from unittest import TestCase
import logging


from utils.patterns import IService
from services.point.creation import PointCreationService
from services.point.update import PointUpdateService
from services.point.exclusion import PointExclusionService
from services.point.capture import PointCaptureService
from services.point.listing import PointListingService
from models import Point


class PointServiceCase(TestCase):
    def test_creation(self) -> None:
        async def main() -> None:
            point_creation_service: IService = PointCreationService(
                company_uuid="f309cbfa-472d-4b29-8cc4-5da7704823d9",
                address_state="SC",
                address_city="Capivari de Baixo",
                address_neighborhood="Centro",
                address_number="000",
                address_street="Centro",
                latitude="-200000",
                longitude="-2000000",
            )

            point: Optional[Point] = await point_creation_service.execute()

            logging.info(f"Point Created: {point}")

    def test_update(self) -> None:
        async def main() -> None:
            point_update_service: IService = PointUpdateService(
                point_uuid="",
                address_state="",
                address_city="",
                address_neighborhood="",
                address_number="",
                address_street="",
                latitude="",
                longitude="",
            )

            point: Optional[Point] = await point_update_service.execute()

            logging.info(f"Point Updated: {point}")

    def test_exclusion(self) -> None:
        async def main() -> None:
            point_exclusion_service: IService = PointExclusionService(point_uuid="")

            point: Optional[Point] = await point_exclusion_service.execute()

            logging.info(f"Point Deleted: {point}")

    def test_listing(self) -> None:
        async def main() -> None:
            point_listing_service: IService = PointListingService(
                company_uuid="", uuids=[]
            )

            points: Sequence[Point] = await point_listing_service.execute()

            logging.info(f"Points: {points}")

            self.assertNotEqual(points, [])

    def test_capture(self) -> None:
        async def main() -> None:
            point_capture_service: IService = PointCaptureService(point_uuid="")

            point: Optional[Point] = await point_capture_service.execute()

            logging.info(f"Point Captured: {point}")

            self.assertNotEqual(point, None)
