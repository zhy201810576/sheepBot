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
from urllib.parse import urljoin

Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

BASE_URL = "https://cn.bing.com"
API_URL = urljoin(BASE_URL, "HPImageArchive.aspx?format=js&idx=0&n=1")


async def get_bing_image() -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=API_URL, headers=Headers, timeout=5) as response:
                res = await response.json(content_type=None)
                info = res["images"][0]
                desc = info["copyright"]
                param_url = info["url"]
                img_url = urljoin(BASE_URL, param_url)
                msg = f'{desc}\n\n[CQ:image,file={img_url},subType=0,cache=0]'
                logger.debug(msg)
                return msg
    except:
        logger.opt(exception=True).error("必应每日一图 - 获取信息失败")
        return "抱歉，信息获取失败啦(っ °Д °;)っ"
