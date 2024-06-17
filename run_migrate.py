from dotenv import load_dotenv
import asyncio


async def main(drop_all: bool = False) -> None:
    from server.instances import ServerInstances
    from server.database import Database
    from utils.constants import DATABASE_INSTANCE_NAME

    import models

    database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

    if drop_all:
        await database.drop_all_async()

    await database.create_all_async()


if __name__ == "__main__":
    load_dotenv()

    asyncio.run(main())
