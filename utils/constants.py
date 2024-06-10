import os

DATABASE_HOST: str = os.environ.get("DATABASE_HOST", "")
DATABASE_PORT: str = os.environ.get("DATABASE_PORT", "")
DATABASE_DBNAME: str = os.environ.get("DATABASE_DBNAME", "")
DATABASE_DIALECT: str = os.environ.get("DATABASE_DIALECT", "")
DATABASE_INSTANCE_NAME: str = os.environ.get("DATABASE_INSTANCE_NAME", "")
DATABASE_USERNAME: str = os.environ.get("DATABASE_USERNAME", "")
DATABASE_PASSWORD: str = os.environ.get("DATABASE_PASSWORD", "")

PUBLIC_API_HOST: str = os.environ.get("PUBLIC_API_HOST", "")
PUBLIC_API_PORT: str = os.environ.get("PUBLIC_API_PORT", "")

PRIVATE_API_HOST: str = os.environ.get("PRIVATE_API_HOST", "")
PRIVATE_API_PORT: str = os.environ.get("PRIVATE_API_PORT", "")

COMPANY_ENPOINT_NAME: str = os.environ.get("COMPANY_ENPOINT_NAME", "")
POINT_ENPOINT_NAME: str = os.environ.get("POINT_ENPOINT_NAME", "")
ROUTE_ENDPOINT_NAME: str = os.environ.get("ROUTE_ENDPOINT_NAME", "")
AGENT_ENDPOINT_NAME: str = os.environ.get("AGENT_ENDPOINT_NAME", "")
AUTH_ENDPOINT_NAME: str = os.environ.get("AUTH_ENDPOINT_NAME", "")

SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
TOKEN_EXPIRATION_MINUTE: int = int(os.environ.get("TOKEN_EXPIRATION_MINUTE", ""))
REFRESH_TOKEN_EXPIRATION_MINUTE: int = int(
    os.environ.get("REFRESH_TOKEN_EXPIRATION_MINUTE", "")
)
