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

Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

URL = "https://api.gmit.vip/Api/FjImg?format=json"


async def get_photo() -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=URL, headers=Headers, timeout=5) as response:
                res = await response.json(content_type=None)
                img_url = res["data"]["url"]
                msg = f'[CQ:image,file={img_url},subType=0,cache=0]'
                logger.debug(msg)
                return msg
    except:
        logger.opt(exception=True).error("风景照 - 获取信息失败")
        return "抱歉，信息获取失败啦(っ °Д °;)っ"
