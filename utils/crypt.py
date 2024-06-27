from typing import Mapping, Any
import bcrypt
import jwt
from datetime import datetime, timedelta, UTC

from utils.entities import TokenDataEntity
from utils.constants import SECRET_KEY


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
            agent_uuid: str,
            company_uuid: str,
            expiration_minute: int,
            is_refresh: bool = False,
        ) -> str:
            expiration: datetime = datetime.now(UTC) + timedelta(
                minutes=expiration_minute
            )

            data: TokenDataEntity = TokenDataEntity(
                agent_uuid=agent_uuid,
                company_uuid=company_uuid,
                exp=expiration,
                is_refresh=is_refresh,
            )

            return jwt.encode(data.model_dump(), SECRET_KEY, "HS256")

        @staticmethod
        def decode_token(token: str) -> TokenDataEntity:
            data: Mapping[str, Any] = jwt.decode(token, SECRET_KEY, ["HS256"])

            token_data: TokenDataEntity = TokenDataEntity(**data)

            if token_data.exp < datetime.now(UTC):
                raise jwt.ExpiredSignatureError()

            return token_data
