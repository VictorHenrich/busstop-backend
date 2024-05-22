from dotenv import load_dotenv
from pathlib import Path
import asyncio

load_dotenv(Path.cwd())


if __name__ == "__main__":
    from server.instances import ServerInstances

    asyncio.run(ServerInstances.run_migrate())
