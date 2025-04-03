from crawl import yandere, posts, tags, artists, comments, wiki, notes, users, forum, pools, favorites
import asyncio


async def main() -> None:
    post = posts()
    await post.download(limit=1000, all_page=True, tags='k-on! horiguchi_yukiko')


if __name__ == "__main__":
    asyncio.run(main())
