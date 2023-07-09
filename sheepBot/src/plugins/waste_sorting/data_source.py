#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" 
---------------------------------------
 # @Project    : sheepBot
 # @File       : data_source.py
 # @Author     : GrayZhao
 # @Date       : 2023/7/8 19:21
 # @Version    : 
 # @Description : 
---------------------------------------
"""
import aiohttp
import asyncio
from nonebot import logger
from urllib.parse import urljoin, quote

Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

BASE_URL = "https://api.vvhan.com/api/la.ji"


async def get_sorted(name: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            _url = urljoin(BASE_URL, f"?lj={quote(name)}")
            async with session.get(url=_url, headers=Headers, timeout=5) as response:
                res = await response.json(content_type=None)
                sort_name = res["sort"]
                msg = f'🗑 物品：{name}\n\n♻ 分类：{sort_name}'
                logger.debug(msg)
                return msg
    except:
        logger.opt(exception=True).error("垃圾分类 - 获取信息失败")
        return "抱歉，信息获取失败啦(っ °Д °;)っ"

