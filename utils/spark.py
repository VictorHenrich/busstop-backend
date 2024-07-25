from typing import Type
from pyspark.sql import SparkSession, DataFrame

from server.database import ServerDatabase
from models.common import BaseModel
from utils.types import DictType
from utils.constants import SPARK_JDBC_URL


class SparkUtils:
    @staticmethod
    def create_session_for_database(
        app_name: str, jdbc_url: str = SPARK_JDBC_URL
    ) -> SparkSession:
        return (
            SparkSession.Builder()
            .appName(app_name)
            .master("spark://localhost:7077")
            .config("spark.jars", jdbc_url)
            .getOrCreate()
        )

    @staticmethod
    def create_dataframe_for_table(
        database: ServerDatabase,
        table: Type[BaseModel],
        spark_session: SparkSession,
        is_async: bool = True,
    ) -> DataFrame:
        dabtase_url: str = database.async_url if is_async is True else database.url

        jdbc_url: str = f"jdbc:{dabtase_url}"

        connection_properties: DictType[str, str] = {"driver": "org.postgresql.Driver"}

        return spark_session.read.jdbc(
            jdbc_url, table.__tablename__, properties=connection_properties
        )
