from dotenv import load_dotenv
from pathlib import Path
import logging


class EnvUtils:
    @staticmethod
    def load_global_envs() -> None:
        env_file = Path().cwd().rglob(".env")

        for env_path in env_file:
            load_dotenv(str(env_path))

            break

        logging.basicConfig(level=logging.INFO)
