from typing import Any, Type, TypeVar
import bcrypt
import jwt
from datetime import datetime, timedelta, UTC

from utils.entities import TokenDataEntity
from utils.config import SECRET_KEY
from utils.types import DictType


T = TypeVar("T", bound=TokenDataEntity)


class CryptUtils:
    class Bcrypt:
        @staticmethod
        def compare_password(password: str, hash: str) -> bool:
            return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))

        @staticmethod
        def create_hash(data: str) -> str:
            return bcrypt.hashpw(data.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    class Jwt:
        @staticmethod
        def create_token(
            user_uuid: str,
            expiration_minute: int,
            is_refresh: bool = False,
            entity_class: Type[T] = TokenDataEntity,
            **kwargs: Any
        ) -> str:
            expiration: datetime = datetime.now(UTC) + timedelta(
                minutes=expiration_minute
            )

            data: T = entity_class(
                user_uuid=user_uuid, exp=expiration, is_refresh=is_refresh, **kwargs
            )

            return jwt.encode(data.model_dump(), SECRET_KEY, "HS256")

        @staticmethod
        def decode_token(token: str, entity_class: Type[T] = TokenDataEntity) -> T:
            data: DictType = jwt.decode(token, SECRET_KEY, ["HS256"])

            token_data: T = entity_class(**data)

            if token_data.exp < datetime.now(UTC):
                raise jwt.ExpiredSignatureError()

            return token_data
