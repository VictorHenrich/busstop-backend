from dotenv import load_dotenv
import asyncio


async def main(drop_all: bool = False) -> None:
    import models

    if drop_all:
        await models.database.drop_all_async()

    await models.database.create_all_async()


if __name__ == "__main__":
    load_dotenv()

    asyncio.run(main())
