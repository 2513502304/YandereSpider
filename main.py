from crawl import Yandere, Posts, Tags, Artists, Comments, Wiki, Notes, Users, Forum, Pools, Favorites
from utils import logger
import asyncio
import time


async def main() -> None:
    start = time.time()
    pool = Pools()
    await pool.download(
        all_page=True,
        query='k-on!',
    )
    end = time.time()
    logger.info(f"Total time taken: {end - start:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
