from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path.cwd())


if __name__ == "__main__":
    from server.instances import ServerInstances

    ServerInstances.run_api()
