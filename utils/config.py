from typing import Sequence
import os

from utils.env import EnvUtils

EnvUtils.load_global_envs()

DATABASE_HOST: str = os.environ.get("DATABASE_HOST", "localhost")
DATABASE_PORT: str = os.environ.get("DATABASE_PORT", "5432")
DATABASE_DBNAME: str = os.environ.get("DATABASE_DBNAME", "busstop_teste")
DATABASE_CURRENT_NAME: str = os.environ.get("DATABASE_CURRENT_NAME", "tests")
DATABASE_USERNAME: str = os.environ.get("DATABASE_USERNAME", "test")
DATABASE_PASSWORD: str = os.environ.get("DATABASE_PASSWORD", "1234")

API_HOST: str = os.environ.get("API_HOST", "")
API_PORT: str = os.environ.get("API_PORT", "")

COMPANY_ENPOINT_NAME: str = os.environ.get("COMPANY_ENPOINT_NAME", "/company")
GEO_ENPOINT_NAME: str = os.environ.get("GEO_ENPOINT_NAME", "/geolocation")
POINT_ENPOINT_NAME: str = os.environ.get("POINT_ENPOINT_NAME", "/point")
ROUTE_ENDPOINT_NAME: str = os.environ.get("ROUTE_ENDPOINT_NAME", "/route")
AGENT_ENDPOINT_NAME: str = os.environ.get("AGENT_ENDPOINT_NAME", "/agent")
USER_ENDPOINT_NAME: str = os.environ.get("USER_ENDPOINT_NAME", "/user")
AUTH_ENDPOINT_NAME: str = os.environ.get("AUTH_ENDPOINT_NAME", "/auth")
DOCS_ENDPOINT_NAME: str = os.environ.get("DOCS_ENDPOINT_NAME", "/docs")
REDOC_ENDPOINT_NAME: str = os.environ.get("REDOC_ENDPOINT_NAME", "/docs")
INDEX_ENDPOINT_NAME: str = os.environ.get("INDEX_ENDPOINT_NAME", "/")
PROFILE_ENDPOINT_NAME: str = os.environ.get("PROFILE_ENDPOINT_NAME", "/profile")
VEHICLE_ENDPOINT_NAME: str = os.environ.get("VEHICLE_ENDPOINT_NAME", "/vehicle")

EVENTS_ENDPOINT_NAME: str = os.environ.get("EVENTS_ENDPOINT_NAME", "")


AGENT_PUBLIC_ROUTES: Sequence[str] = (
    DOCS_ENDPOINT_NAME,
    REDOC_ENDPOINT_NAME,
    AUTH_ENDPOINT_NAME,
)

USER_PUBLIC_ROUTES: Sequence[str] = AUTH_ENDPOINT_NAME

SECRET_KEY: str = os.environ.get("SECRET_KEY", "test123")
TOKEN_EXPIRATION_MINUTE: int = int(os.environ.get("TOKEN_EXPIRATION_MINUTE", "5"))
REFRESH_TOKEN_EXPIRATION_MINUTE: int = int(
    os.environ.get("REFRESH_TOKEN_EXPIRATION_MINUTE", "10")
)

SWAGGER_API_TITLE: str = os.environ.get("SWAGGER_API_TITLE", "")
SWAGGER_AGENT_API_TITLE: str = os.environ.get("SWAGGER_AGENT_API_TITLE", "")
SWAGGER_USER_API_TITLE: str = os.environ.get("SWAGGER_USER_API_TITLE", "")
SWAGGER_API_DESCRIPTION: str = os.environ.get("SWAGGER_API_DESCRIPTION", "")
SWAGGER_AGENT_API_DESCRIPTION: str = os.environ.get("SWAGGER_AGENT_API_DESCRIPTION", "")
SWAGGER_USER_API_DESCRIPTION: str = os.environ.get("SWAGGER_USER_API_DESCRIPTION", "")
SWAGGER_API_VERSION: str = os.environ.get("SWAGGER_API_VERSION", "")
SWAGGER_POINT_SESSION_TAG: str = os.environ.get("SWAGGER_POINT_SESSION_TAG", "")
SWAGGER_ROUTE_SESSION_TAG: str = os.environ.get("SWAGGER_ROUTE_SESSION_TAG", "")
SWAGGER_GEO_SESSION_TAG: str = os.environ.get("SWAGGER_GEO_SESSION_TAG", "")
SWAGGER_COMPANY_SESSION_TAG: str = os.environ.get("SWAGGER_COMPANY_SESSION_TAG", "")
SWAGGER_PROFILE_SESSION_TAG: str = os.environ.get("SWAGGER_PROFILE_SESSION_TAG", "")
SWAGGER_AUTH_SESSION_TAG: str = os.environ.get("SWAGGER_AUTH_SESSION_TAG", "")
SWAGGER_INDEX_SESSION_TAG: str = os.environ.get("SWAGGER_INDEX_SESSION_TAG", "")
SWAGGER_EVENTS_SESSION_TAG: str = os.environ.get("SWAGGER_EVENTS_SESSION_TAG", "")

GOOGLE_API_KEY: str = os.environ.get("GOOGLE_API_KEY", "")
GOOGLE_API_URL: str = os.environ.get("GOOGLE_API_URL", "")

TYPE_ADDRESS_ZIP_CODE: str = os.environ.get("TYPE_ADDRESS_ZIP_CODE", "")
TYPE_ADDRESS_STATE: str = os.environ.get("TYPE_ADDRESS_STATE", "")
TYPE_ADDRESS_CITY: str = os.environ.get("TYPE_ADDRESS_CITY", "")
TYPE_ADDRESS_NEIGHBORHOOD: str = os.environ.get("TYPE_ADDRESS_NEIGHBORHOOD", "")
TYPE_ADDRESS_STREET: str = os.environ.get("TYPE_ADDRESS_STREET", "")
TYPE_ADDRESS_NUMBER: str = os.environ.get("TYPE_ADDRESS_NUMBER", "")

SPARK_JDBC_URL: str = os.environ.get("SPARK_JDBC_URL", "")

BROKER_KAFKA_URL: str = os.environ.get("BROKER_KAFKA_URL", "localhost:9092")
