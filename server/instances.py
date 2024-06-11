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
    DOCS_ENDPOINT_NAME,
    REDOC_ENDPOINT_NAME,
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

    api: Api = Api(
        host=API_HOST,
        port=API_PORT,
        docs_url=DOCS_ENDPOINT_NAME,
        redoc_url=REDOC_ENDPOINT_NAME,
        title="API BUSSTOP",
    )
