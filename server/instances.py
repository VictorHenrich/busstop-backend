from server.api import Api
from server.database import Databases, Database, DatabaseDialects
from utils.constants import (
    API_HOST,
    API_PORT,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DBNAME,
    DATABASE_DIALECT,
    DATABASE_INSTANCE_NAME,
    DATABASE_PASSWORD,
    DATABASE_USERNAME,
)


class ServerInstances:
    databases: Databases = Databases(
        Database(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            dbname=DATABASE_DBNAME,
            username=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
            dialect=DatabaseDialects(DATABASE_DIALECT),
            instance_name=DATABASE_INSTANCE_NAME,
        )
    )

    api: Api = Api(host=API_HOST, port=API_PORT)

    @classmethod
    def run_api(cls):
        cls.api.start()

    @classmethod
    async def run_migrate(cls, drop_all: bool = False):
        database: Database = cls.databases.select(DATABASE_INSTANCE_NAME)

        if drop_all:
            await database.drop_all_async()

        await database.create_all_async()
