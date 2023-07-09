#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" 
---------------------------------------
 # @Project    : sheepBot
 # @File       : data_source.py
 # @Author     : GrayZhao
 # @Date       : 2023/7/7 14:10
 # @Version    : 
 # @Description : 
---------------------------------------
"""
import aiohttp
import asyncio
from nonebot import logger
from nonebot.adapters.onebot.v11 import MessageSegment

Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

URL = "https://api.emoao.com/api/moyu?type=json"


async def fetch_final_url(url: str) -> str:
    """获取直到不再跳转的url链接"""
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url, allow_redirects=False) as response:
                if response.status == 200:
                    return response.url.human_repr()
                elif response.status in [301, 302, 303, 307, 308]:
                    url = response.headers.get('Location')
                    if not url:
                        return url
                else:
                    return url


async def get_moyu() -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=URL, headers=Headers, timeout=5) as response:
                res = await response.json(content_type=None)
                title = res["title"]
                img_url = await fetch_final_url(res["imgurl"])
                msg = f'{title}\n\n{MessageSegment.image(img_url)}'
                logger.debug(msg)
                return msg
    except:
        logger.opt(exception=True).error("摸鱼人日历 - 获取信息失败")
        return "抱歉，信息获取失败啦(っ °Д °;)っ"
