from utils import logger

from fake_useragent import UserAgent
from urllib.parse import quote, unquote
import httpx

from aiofiles import os as aioos
from aiofiles import tempfile as aiotempfile
import aiofiles

import pandas as pd

import os


class yandere:
    """
    Yandere API reference document: https://yande.re/help/api
    """

    def __init__(self):
        self.headers = {
            'User-Agent': UserAgent().random,
        }
        self.params = {}
        self.client = httpx.AsyncClient(
            headers=self.headers,
            params=self.params,
            base_url='https://yande.re',
        )

    async def download_file(self, urls: pd.Series, directory: str) -> None:
        """
        下载文件到指定目录，忽略已存在的文件

        Args:
            urls (pd.Series): 文件 URLs
            directory (str): 文件存储目录
        """
        # 创建目录
        if not os.path.exists(directory):
            os.makedirs(directory)
        # 若存在已有文件，则将其过滤
        else:
            # 获取已有文件列表
            files = os.listdir(directory)
            # 过滤已有文件
            urls = urls[~urls.apply(lambda x: os.path.basename(x) in files)]
        # 检查 URLs 是否为空
        if urls.empty:
            return
        # 下载文件
        headers = {
            'User-Agent': UserAgent().random,
        }
        params = {}
        # 遍历 URLs
        for url in urls:
            # 获取文件名
            filename = os.path.join(directory, os.path.basename(url))
            # 下载文件
            response = await self.client.get(url, headers=headers, params=params)
            # 保存文件
            async with aiofiles.open(filename, 'wb') as f:
                await f.write(response.content)

    @staticmethod
    def parse_url(url: str) -> str:
        """
        解析文件链接 URL，并将其转换为用户可读的规范化名称

        Args:
            url (str): 文件 URL

        Returns:
            str: 用户可读的规范化名称
            
        Example:
            帖子链接：https://yande.re/post/show/1023280  
            帖子标签：horiguchi_yukiko k-on! akiyama_mio hirasawa_yui kotobuki_tsumugi nakano_azusa tainaka_ritsu cleavage disc_cover dress summer_dress screening  
            帖子下载链接：https://files.yande.re/image/c0abd1a95b5e9f9ed845e24ffb0f663d/yande.re%201023280%20akiyama_mio%20cleavage%20disc_cover%20dress%20hirasawa_yui%20horiguchi_yukiko%20k-on%21%20kotobuki_tsumugi%20nakano_azusa%20screening%20summer_dress%20tainaka_ritsu.jpg  
            
            处理过程：
            - 获取帖子下载链接的基础名称（即帖子下载链接的最后一个组件）：yande.re%201023280%20akiyama_mio%20cleavage%20disc_cover%20dress%20hirasawa_yui%20horiguchi_yukiko%20k-on%21%20kotobuki_tsumugi%20nakano_azusa%20screening%20summer_dress%20tainaka_ritsu.jpg
            - 解码经过 url 编码后的基础名称：yande.re 1023280 akiyama_mio cleavage disc_cover dress hirasawa_yui horiguchi_yukiko k-on! kotobuki_tsumugi nakano_azusa screening summer_dress tainaka_ritsu.jpg
        
        Note:
            - yandere 文件命名规则为：yande.re {帖子 ID} {按照 a-z 排序后的标签}.文件后缀名
            - 永远不要使用该方法返回的规范化名称作为存储文件的文件名，因为解码经过 url 编码后的基础名称中，可能包含非法字符（在按照 a-z 排序后的标签中，可能包含 ： < > : " / \ | ? * 等 Windows 系统中的非法字符，从而引发 OSError: [WinError 123] 文件名、目录名或卷标语法不正确）
        """
        # 帖子下载链接的基础名称
        basename = os.path.basename(url)
        # 解码 url 编码后的基础名称（此步骤等同于将 %20 解码为空格，将 %21 解码为 !）
        decoded_basename = unquote(basename)  # basename.replace('%20', ' ').replace('%21', '!')
        return decoded_basename


class posts(yandere):
    """
    Posts: https://yande.re/help/api#posts
    """

    def __init__(self):
        super().__init__()

    async def list(self, limit: int = 40, start_page: int = 1, end_page: int = 1, all_page: bool = False, tags: str = '') -> pd.DataFrame:
        """
        List
        
        The base URL is /post.xml.
        
        - limit: How many posts you want to retrieve. There is a hard limit of 100 posts per request.
        - page: The page number.
        - tags: The tags to search for. Any tag combination that works on the web site will work here. This includes all the meta-tags.

        Note: 修订 API 参考文件: https://yande.re/help/api: limit: How many posts you want to retrieve. There is a hard limit of 100 posts per request. 将其更改为：limit: How many posts you want to retrieve. There is a hard limit of 1000 posts per request.
        
        Return json format:
        ```
        [
            {
                "id": 1223391,
                "tags": "akiyama_mio bleed_through chibi christmas dress fixme hirasawa_yui horiguchi_yukiko k-on! kotobuki_tsumugi nakano_azusa pantyhose tainaka_ritsu",
                "created_at": 1742150809,
                "updated_at": 1742156680,
                "creator_id": 537635,
                "approver_id": null,
                "author": "Reverseshin",
                "change": 6324472,
                "source": "Animedia 2010-12",
                "score": 3,
                "md5": "3a453ffae99c4de46e4fb5bf82236842",
                "file_size": 26463488,
                "file_ext": "png",
                "file_url": "https://files.yande.re/image/3a453ffae99c4de46e4fb5bf82236842/yande.re%201223391%20akiyama_mio%20bleed_through%20chibi%20christmas%20dress%20fixme%20hirasawa_yui%20horiguchi_yukiko%20k-on%21%20kotobuki_tsumugi%20nakano_azusa%20pantyhose%20tainaka_ritsu.png",
                "is_shown_in_index": false,
                "preview_url": "https://assets.yande.re/data/preview/3a/45/3a453ffae99c4de46e4fb5bf82236842.jpg",
                "preview_width": 150,
                "preview_height": 93,
                "actual_preview_width": 300,
                "actual_preview_height": 186,
                "sample_url": "https://files.yande.re/sample/3a453ffae99c4de46e4fb5bf82236842/yande.re%201223391%20sample%20akiyama_mio%20bleed_through%20chibi%20christmas%20dress%20fixme%20hirasawa_yui%20horiguchi_yukiko%20k-on%21%20kotobuki_tsumugi%20nakano_azusa%20pantyhose%20tainaka_ritsu.jpg",
                "sample_width": 1500,
                "sample_height": 931,
                "sample_file_size": 481240,
                "jpeg_url": "https://files.yande.re/jpeg/3a453ffae99c4de46e4fb5bf82236842/yande.re%201223391%20akiyama_mio%20bleed_through%20chibi%20christmas%20dress%20fixme%20hirasawa_yui%20horiguchi_yukiko%20k-on%21%20kotobuki_tsumugi%20nakano_azusa%20pantyhose%20tainaka_ritsu.jpg",
                "jpeg_width": 3500,
                "jpeg_height": 2172,
                "jpeg_file_size": 2088523,
                "rating": "s",
                "is_rating_locked": false,
                "has_children": false,
                "parent_id": 162305,
                "status": "active",
                "is_pending": false,
                "width": 5492,
                "height": 3408,
                "is_held": false,
                "frames_pending_string": "",
                "frames_pending": [],
                "frames_string": "",
                "frames": [],
                "is_note_locked": false,
                "last_noted_at": 0,
                "last_commented_at": 0
            },
            ...
        ]
        ```

        获取在起始页码与结束页码范围内，指定标签的帖子列表；若 all_page 为 True，则获取当前查询标签下所有页码的帖子列表
        
        Args:
            limit (int, optional): 您想检索多少篇帖子。每次请求的帖子数量有一个硬性限制，最多 1000 篇. Defaults to 40.
            start_page (int, optional): 查询起始页码. Defaults to 1.
            end_page (int, optional): 查询结束页码. Defaults to 1.
            all_page (bool, optional): 是否获取当前查询标签下所有页码的帖子列表，若为 True，则忽略 start_page 与 end_page 参数. Defaults to False.
            tags (str, optional): 要搜索的标签。任何在网站上有效的标签组合在这里都有效。这包括所有元标签。要组合的不同标签使用空格连接，同一标签中的空格使用 _ 替换. Defaults to ''.

        Returns:
            pd.DataFrame: 请求结果列表
        """
        url = '/post.json'
        headers = {
            'User-Agent': UserAgent().random,
        }
        params = {
            'limit': limit,  # 您想检索多少篇帖子。每次请求的帖子数量有一个硬性限制，最多 1000 篇
            'page': 1,  # 查询页码
            'tags': tags,  # 要搜索的标签。任何在网站上有效的标签组合在这里都有效。这包括所有元标签。要组合的不同标签使用空格连接，同一标签中的空格使用 _ 替换
        }
        # 结果列表
        result: list[dict] = []
        # 获取当前查询标签下所有页码的帖子列表
        if all_page:
            # 当前查询页码
            page = 1
            # 直到获取到空数据为止
            while True:
                params.update({'page': page})
                response = await self.client.get(url, headers=headers, params=params)
                content: list[dict] = response.json()
                if content:
                    result.extend(content)
                    page += 1
                else:
                    break
        # 获取在起始页码与结束页码范围内，指定标签的帖子列表
        else:
            # 获取指定页码的帖子列表
            for page in range(start_page, end_page + 1):
                params.update({'page': page})
                response = await self.client.get(url, headers=headers, params=params)
                content: list[dict] = response.json()
                if content:
                    result.extend(content)
                else:
                    break
        return pd.DataFrame(result)

    def create(self, ):
        # TODO
        pass

    def update(self, ):
        # TODO
        pass

    def destroy(self, ):
        # TODO
        pass

    def revert_tags(self, ):
        # TODO
        pass

    def vote(self, ):
        # TODO
        pass

    async def download(self, limit: int = 40, start_page: int = 1, end_page: int = 1, all_page: bool = False, tags: str = '') -> None:
        """
        下载在起始页码与结束页码范围内，指定标签的帖子列表中的帖子；若 all_page 为 True，则下载当前查询标签下所有页码的帖子列表中的帖子

        Args:
            limit (int, optional): 您想检索多少篇帖子。每次请求的帖子数量有一个硬性限制，最多 1000 篇. Defaults to 40.
            start_page (int, optional): 查询起始页码. Defaults to 1.
            end_page (int, optional): 查询结束页码. Defaults to 1.
            all_page (bool, optional): 是否获取当前查询标签下所有页码的帖子列表，若为 True，则忽略 start_page 与 end_page 参数. Defaults to False.
            tags (str, optional): 要搜索的标签。任何在网站上有效的标签组合在这里都有效。这包括所有元标签。要组合的不同标签使用空格连接，同一标签中的空格使用 _ 替换. Defaults to ''.
        """
        # 获取当前查询标签下所有页码的帖子列表中的帖子
        posts = await self.list(limit=limit, start_page=start_page, end_page=end_page, all_page=all_page, tags=tags)
        # 帖子 URLs
        urls = posts['file_url']
        # 存储文件路径
        path = f'./downloads/posts/{tags}'
        # 下载文件
        await self.download_file(urls, path)


class tags(yandere):
    """
    Tags: https://yande.re/help/api#tags
    """

    def __init__(self):
        super().__init__()

    def list(self, ):
        # TODO
        pass

    def update(self, ):
        # TODO
        pass

    def related(self, ):
        # TODO
        pass


class artists(yandere):
    """
    Artists: https://yande.re/help/api#artists
    """

    def __init__(self):
        super().__init__()

    def list(self, ):
        # TODO
        pass

    def create(self, ):
        # TODO
        pass

    def update(self, ):
        # TODO
        pass

    def destroy(self, ):
        # TODO
        pass


class comments(yandere):
    """
    Comments: https://yande.re/help/api#comments
    """

    def __init__(self):
        super().__init__()

    def show(self, ):
        # TODO
        pass

    def create(self, ):
        # TODO
        pass

    def destory(self, ):
        # TODO
        pass


class wiki(yandere):
    """
    Wiki: https://yande.re/help/api#wiki
    """

    def __init__(self):
        super().__init__()

    def list(self, ):
        # TODO
        pass

    def create(self, ):
        # TODO
        pass

    def update(self, ):
        # TODO
        pass

    def show(self, ):
        # TODO
        pass

    def destroy(self, ):
        # TODO
        pass

    def lock(self, ):
        # TODO
        pass

    def unlock(self, ):
        # TODO
        pass

    def revert(self, ):
        # TODO
        pass

    def history(self, ):
        # TODO
        pass


class notes(yandere):
    """
    Notes: https://yande.re/help/api#notes
    """

    def __init__(self):
        super().__init__()

    def list(self, ):
        # TODO
        pass

    def search(self, ):
        # TODO
        pass

    def history(self, ):
        # TODO
        pass

    def revert(self, ):
        # TODO
        pass

    def create(self, ):
        # TODO
        pass

    def update(self, ):
        # TODO
        pass


class users(yandere):
    """
    Users: https://yande.re/help/api#users
    """

    def __init__(self):
        super().__init__()

    def search(self, ):
        # TODO
        pass


class forum(yandere):
    """
    Forum: https://yande.re/help/api#forum
    """

    def __init__(self):
        super().__init__()

    def list(self, ):
        # TODO
        pass


class pools(yandere):
    """
    Pools: https://yande.re/help/api#pools
    """

    def __init__(self):
        super().__init__()

    async def list_pools(self, query: str, start_page: int = 1, end_page: int = 1, all_page: bool = False) -> pd.DataFrame:
        """
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
        # 获取当前查询标题下所有页码的图集列表
        if all_page:
            # 当前查询页码
            page = 1
            # 直到获取到空数据为止
            while True:
                params.update({'page': page})
                response = await self.client.get(url, headers=headers, params=params)
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
                response = await self.client.get(url, headers=headers, params=params)
                content: list[dict] = response.json()
                if content:
                    result.extend(content)
                else:
                    break
        return pd.DataFrame(result)

    async def list_posts(self, id: int, start_page: int = 1, end_page: int = 1, all_page: bool = False) -> pd.DataFrame:
        """
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
        # 获取当前图集 ID 下所有页码的帖子列表
        if all_page:
            # 当前查询页码
            page = 1
            # 直到获取到空数据为止
            while True:
                params.update({'page': page})
                response = await self.client.get(url, headers=headers, params=params)
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
                response = await self.client.get(url, headers=headers, params=params)
                content: dict = response.json()
                posts: list[dict] = content.get('posts', [])
                if posts:
                    result.extend(posts)
                else:
                    break
        return pd.DataFrame(result)

    def update_pool(self, ):
        # TODO
        pass

    def create_pool(self, ):
        # TODO
        pass

    def destroy_pool(self, ):
        # TODO
        pass

    def add_post(self, ):
        # TODO
        pass

    def remove_post(self, ):
        # TODO
        pass

    async def download(self, query: str, start_page: int = 1, end_page: int = 1, all_page: bool = False) -> None:
        """
        下载在起始页码与结束页码范围内，指定标题的图集列表中的帖子；若 all_page 为 True，则下载当前查询标题下所有页码的图集列表中的帖子

        Args:
            query (str): 查询标题
            start_page (int, optional): 查询起始页码. Defaults to 1.
            end_page (int, optional): 查询结束页码. Defaults to 1.
            all_page (bool, optional): 是否下载当前查询标题下所有页码的图集列表中的帖子，若为 True，则忽略 start_page 与 end_page 参数. Defaults to False.
        """
        # 获取当前查询标题下所有页码的图集列表
        pools = await self.list_pools(query=query, start_page=start_page, end_page=end_page, all_page=all_page)
        # 图集 id
        ids = pools['id']
        # 图集名称
        names = pools['name']
        # 遍历图集列表
        for id, name in zip(ids, names):
            # 获取图集 ID 下所有帖子
            posts = await self.list_posts(id=id, start_page=start_page, end_page=end_page, all_page=all_page)
            # 获取帖子 URLs
            urls = posts['file_url']
            # 存储文件路径
            path = f'./downloads/pools/{name}'
            # 下载文件
            await self.download_file(urls, path)


class favorites(yandere):
    """
    Favorites: https://yande.re/help/api#favorites
    """

    def __init__(self):
        super().__init__()

    def list_users(self, ):
        # TODO
        pass
