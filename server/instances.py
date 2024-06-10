from server.api import Api
from server.database import Databases, Database, DatabaseDialects
from utils.constants import (
    PUBLIC_API_HOST,
    PUBLIC_API_PORT,
    PRIVATE_API_HOST,
    PRIVATE_API_PORT,
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

    public_api: Api = Api(host=PUBLIC_API_HOST, port=PUBLIC_API_PORT)

    private_api: Api = Api(host=PRIVATE_API_HOST, port=PRIVATE_API_PORT)
