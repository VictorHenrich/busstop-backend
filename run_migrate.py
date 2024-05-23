from dotenv import load_dotenv
import asyncio


if __name__ == "__main__":
    load_dotenv()

    from server.instances import ServerInstances

    asyncio.run(ServerInstances.run_migrate(drop_all=True))
