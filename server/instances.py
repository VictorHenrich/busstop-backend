from server.api import ServerApi
from server.database import ServerDatabases, ServerDatabase
from utils.types import DatabaseDialectType
from utils.config import (
    API_HOST,
    API_PORT,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DBNAME,
    DATABASE_PASSWORD,
    DATABASE_USERNAME,
    DOCS_ENDPOINT_NAME,
    REDOC_ENDPOINT_NAME,
    SWAGGER_API_DESCRIPTION,
    SWAGGER_API_TITLE,
    SWAGGER_API_VERSION,
    SWAGGER_AGENT_API_TITLE,
    SWAGGER_USER_API_TITLE,
    SWAGGER_AGENT_API_DESCRIPTION,
    SWAGGER_USER_API_DESCRIPTION,
)


class ServerInstances:
    databases: ServerDatabases = ServerDatabases(
        ServerDatabase(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            dbname=DATABASE_DBNAME,
            username=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
            dialect=DatabaseDialectType.POSTGRESQL,
            instance_name="main",
        ),
        ServerDatabase(
            host="",
            port="",
            dbname="",
            username="",
            password="",
            in_memory=True,
            dialect=DatabaseDialectType.SQLITE,
            instance_name="tests",
        ),
    )

    user_api: ServerApi = ServerApi(
        host=API_HOST,
        port=API_PORT,
        docs_url=DOCS_ENDPOINT_NAME,
        redoc_url=REDOC_ENDPOINT_NAME,
        title=SWAGGER_USER_API_TITLE,
        description=SWAGGER_USER_API_DESCRIPTION,
        version=SWAGGER_API_VERSION,
    )

    agent_api: ServerApi = ServerApi(
        host=API_HOST,
        port=API_PORT,
        docs_url=DOCS_ENDPOINT_NAME,
        redoc_url=REDOC_ENDPOINT_NAME,
        title=SWAGGER_AGENT_API_TITLE,
        description=SWAGGER_AGENT_API_DESCRIPTION,
        version=SWAGGER_API_VERSION,
    )

    general_api: ServerApi = ServerApi(
        host=API_HOST,
        port=API_PORT,
        docs_url=DOCS_ENDPOINT_NAME,
        redoc_url=REDOC_ENDPOINT_NAME,
        title=SWAGGER_API_TITLE,
        description=SWAGGER_API_DESCRIPTION,
        version=SWAGGER_API_VERSION,
    )
