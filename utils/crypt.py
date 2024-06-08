import bcrypt


class CryptUtils:
    @staticmethod
    def bcrypt_compare_password(password: str, hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))

    @staticmethod
    def bcrypt_create_hash(data: str) -> str:
        return bcrypt.hashpw(data.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
