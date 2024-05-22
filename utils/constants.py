import os

DATABASE_HOST: str = os.environ.get("DATABASE_HOST", "")

DATABASE_PORT: str = os.environ.get("DATABASE_PORT", "")

DATABASE_DBNAME: str = os.environ.get("DATABASE_DBNAME", "")

DATABASE_DIALECT: str = os.environ.get("DATABASE_DIALECT", "")

DATABASE_INSTANCE_NAME: str = os.environ.get("DATABASE_INSTANCE_NAME", "")

DATABASE_USERNAME: str = os.environ.get("DATABASE_USERNAME", "")

DATABASE_PASSWORD: str = os.environ.get("DATABASE_PASSWORD", "")

API_HOST: str = os.environ.get("API_HOST", "")

API_PORT: str = os.environ.get("API_PORT", "")
