#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" 
---------------------------------------
 # @Project    : sheepBot
 # @File       : data_source.py
 # @Author     : GrayZhao
 # @Date       : 2023/7/6 23:51
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

URL = "https://api.emoao.com/api/lsjr"


async def get_today_in_history() -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=URL, headers=Headers, timeout=5) as response:
                res = await response.json(content_type=None)
                day = res["day"]
                results = res["result"]
                msg = f'今天是：{day}\n\n\n'
                interval = len(results) - 1
                count = 0
                for element in results:
                    line = f'{element["year"]} - {element["title"]}'
                    msg = msg + line
                    count += 1
                    if count <= interval:
                        msg = msg + "\n\n"
                logger.debug(msg)
                return msg
    except:
        logger.opt(exception=True).error("历史上的今天 - 获取信息失败")
        return "抱歉，信息获取失败啦(っ °Д °;)っ"
