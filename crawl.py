"""
API 参考文件: https://yande.re/help/api
"""
from utils import logger

from fake_useragent import UserAgent
import httpx

from aiofiles import os as aioos
from aiofiles import tempfile as aiotempfile
import aiofiles

import pandas as pd

import os


async def list_pools(query: str, start_page: int = 1, end_page: int = 1, all_page: bool = False) -> pd.DataFrame:
    """
    Pools: https://yande.re/help/api#pools
    
    List Pools
    
    The base URL is /pool.xml. If you don't specify any parameters you'll get a list of all pools.
    - query: The title.
    - page: The page.
    
    Return json format:
    ```
    [
        {
            "id": 1746,
            "name": "K-ON!_-_Colorful_Memories",
            "created_at": "2010-07-18T00:21:15.758Z",
            "updated_at": "2012-03-11T19:10:27.707Z",
            "user_id": 3048,
            "is_public": true,
            "post_count": 44,
            "description": "http://kyotoanimation.shop-pro.jp/?pid=20190414"
        },
        ...
    ]
    ```
  
    获取在起始页码与结束页码范围内，指定标题的图集列表；若 all_page 为 True，则获取当前查询标题下所有页码的图集列表

    Args:
        query (str): 查询标题
        start_page (int, optional): 查询起始页码. Defaults to 1.
        end_page (int, optional): 查询结束页码. Defaults to 1.
        all_page (bool, optional): 是否获取当前查询标题下所有页码的图集列表，若为 True，则忽略 start_page 与 end_page 参数. Defaults to False.

    Returns:
        pd.DataFrame: 请求结果列表
    """
    url = '/pool.json'
    headers = {
        'User-Agent': UserAgent().random,
    }
    params = {
        'query': query,  # 查询标题
        'page': 1,  # 查询页码
    }
    # 结果列表
    result: list[dict] = []
    # 发起请求
    async with httpx.AsyncClient(headers=headers, params=params, base_url='https://yande.re') as client:
        # 获取当前查询标题下所有页码的图集列表
        if all_page:
            # 当前查询页码
            page = 1
            # 直到获取到空数据为止
            while True:
                params.update({'page': page})
                response = await client.get(url, headers=headers, params=params)
                content: list[dict] = response.json()
                if content:
                    result.extend(content)
                    page += 1
                else:
                    break
        # 获取在起始页码与结束页码范围内，指定标题的图集列表
        else:
            # 获取指定页码的图集列表
            for page in range(start_page, end_page + 1):
                params.update({'page': page})
                response = await client.get(url, headers=headers, params=params)
                content: list[dict] = response.json()
                if content:
                    result.extend(content)
                else:
                    break
    return pd.DataFrame(result)


async def list_posts(id: int, start_page: int = 1, end_page: int = 1, all_page: bool = False) -> pd.DataFrame:
    """
    Pools: https://yande.re/help/api#pools
    
    List Posts
    
    The base URL is /pool/show.xml. If you don't specify any parameters you'll get a list of all pools.
    
    Note: 修订 API 参考文件: https://yande.re/help/api: If you don't specify any parameters you'll get a list of all pools. 将其更改为：If you don't specify any parameters you'll get a list of pool which id is 0.

    - id: The pool id number.
    - page: The page.
    
    Return json format:
    ```
    {
        "id": 1746,
        "name": "K-ON!_-_Colorful_Memories",
        "created_at": "2010-07-18T00:21:15.758Z",
        "updated_at": "2012-03-11T19:10:27.707Z",
        "user_id": 3048,
        "is_public": true,
        "post_count": 44,
        "description": "http://kyotoanimation.shop-pro.jp/?pid=20190414",
        "posts": [
            {
                "id": 145519,
                "tags": "akiyama_mio hirasawa_yui jpeg_artifacts k-on! kotobuki_tsumugi nakano_azusa pantyhose tainaka_ritsu",
                "created_at": "2010-07-18T00:23:44.162Z",
                "creator_id": 17990,
                "author": "Share",
                "change": 650971,
                "source": "",
                "score": 30,
                "md5": "841ac093c4e6de2dd13ce1fb52703da7",
                "file_size": 1143459,
                "file_url": "https://files.yande.re/image/841ac093c4e6de2dd13ce1fb52703da7/yande.re%20145519%20akiyama_mio%20hirasawa_yui%20jpeg_artifacts%20k-on%21%20kotobuki_tsumugi%20nakano_azusa%20pantyhose%20tainaka_ritsu.jpg",
                "is_shown_in_index": true,
                "preview_url": "https://assets.yande.re/data/preview/84/1a/841ac093c4e6de2dd13ce1fb52703da7.jpg",
                "preview_width": 106,
                "preview_height": 150,
                "actual_preview_width": 213,
                "actual_preview_height": 300,
                "sample_url": "https://files.yande.re/sample/841ac093c4e6de2dd13ce1fb52703da7/yande.re%20145519%20sample%20akiyama_mio%20hirasawa_yui%20jpeg_artifacts%20k-on%21%20kotobuki_tsumugi%20nakano_azusa%20pantyhose%20tainaka_ritsu.jpg",
                "sample_width": 1065,
                "sample_height": 1500,
                "sample_file_size": 271128,
                "jpeg_url": "https://files.yande.re/image/841ac093c4e6de2dd13ce1fb52703da7/yande.re%20145519%20akiyama_mio%20hirasawa_yui%20jpeg_artifacts%20k-on%21%20kotobuki_tsumugi%20nakano_azusa%20pantyhose%20tainaka_ritsu.jpg",
                "jpeg_width": 3000,
                "jpeg_height": 4226,
                "jpeg_file_size": 0,
                "rating": "s",
                "has_children": false,
                "parent_id": null,
                "status": "active",
                "width": 3000,
                "height": 4226,
                "is_held": false,
                "frames_pending_string": "",
                "frames_pending": [],
                "frames_string": "",
                "frames": []
            },
            ...
        ]
    }
    ```
    
    获取在起始页码与结束页码范围内，指定图集 ID 的帖子列表；若 all_page 为 True，则获取当前图集 ID 下所有页码的帖子列表

    Args:
        id (int): 图集的 ID 号码
        start_page (int, optional): 查询起始页码. Defaults to 1.
        end_page (int, optional): 查询结束页码. Defaults to 1.
        all_page (bool, optional): 是否获取当前图集 ID 下所有页码的帖子列表，若为 True，则忽略 start_page 与 end_page 参数. Defaults to False.
        
    Returns:
        pd.DataFrame: 请求结果列表
    """
    url = '/pool/show.json'
    headers = {
        'User-Agent': UserAgent().random,
    }
    params = {
        'id': id,  # 图集的 ID 号码
        'page': 1,  # 查询页码
    }
    # 结果列表
    result: list[dict] = []
    # 发起请求
    async with httpx.AsyncClient(headers=headers, params=params, base_url='https://yande.re') as client:
        # 获取当前图集 ID 下所有页码的帖子列表
        if all_page:
            # 当前查询页码
            page = 1
            # 直到获取到空数据为止
            while True:
                params.update({'page': page})
                response = await client.get(url, headers=headers, params=params)
                content: dict = response.json()
                posts: list[dict] = content.get('posts', [])
                if posts:
                    result.extend(posts)
                    page += 1
                else:
                    break
        # 获取在起始页码与结束页码范围内，指定图集 ID 的帖子列表
        else:
            # 获取指定页码的帖子列表
            for page in range(start_page, end_page + 1):
                params.update({'page': page})
                response = await client.get(url, headers=headers, params=params)
                content: dict = response.json()
                posts: list[dict] = content.get('posts', [])
                if posts:
                    result.extend(posts)
                else:
                    break
    return pd.DataFrame(result)


def pool_update():
    # TODO
    pass


def pool_create():
    # TODO
    pass


def pool_destroy():
    # TODO
    pass


def add_post():
    # TODO
    pass


def remove_post():
    # TODO
    pass


async def download_file(urls: pd.Series, directory: str) -> None:
    """
    下载文件到指定目录

    Args:
        urls (pd.Series): 文件 URLs
        directory (str): 文件存储目录
    """
    # 创建目录
    if not os.path.exists(directory):
        os.makedirs(directory)
    # 检查 URLs 是否为空
    if urls.empty:
        return
    # 下载文件
    headers = {
        'User-Agent': UserAgent().random,
    }
    params = {}
    async with httpx.AsyncClient(headers=headers, params=params) as client:
        # 遍历 URLs
        for url in urls:
            # 获取文件名
            filename = os.path.join(directory, os.path.basename(url))
            # 下载文件
            response = await client.get(url, headers=headers, params=params)
            # 保存文件
            async with aiofiles.open(filename, 'wb') as f:
                await f.write(response.content)
