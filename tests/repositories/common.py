from unittest import IsolatedAsyncioTestCase

from models import database


class BaseRepositoryTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        await database.create_all_async()

    async def asyncTearDown(self) -> None:
        await database.drop_all_async()
