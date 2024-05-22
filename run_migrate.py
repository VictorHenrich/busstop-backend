from dotenv import load_dotenv
from pathlib import Path
import asyncio


if __name__ == "__main__":
    load_dotenv(Path.cwd())

    from server.instances import ServerInstances

    import models.company
    import models.point
    import models.route
    import models.route_point

    asyncio.run(ServerInstances.run_migrate())
