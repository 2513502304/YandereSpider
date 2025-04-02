from crawl import list_pools, list_posts, pool_update, pool_create, pool_destroy, add_post, remove_post, download_file
import asyncio


async def main() -> None:
    # 获取当前查询标题下所有页码的图集列表
    pools = await list_pools('k-on', all_page=True)
    # 遍历图集列表
    for id in pools['id']:
        # 获取图集 ID 下所有帖子
        posts = await list_posts(id, all_page=True)
        # 获取文件 URLs
        urls = posts['file_url']
        # 下载文件
        await download_file(urls, f'./downloads/{id}')


if __name__ == "__main__":
    asyncio.run(main())
