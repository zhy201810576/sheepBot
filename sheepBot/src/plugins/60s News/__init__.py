#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" 
---------------------------------------
 # @Project    : sheepBot
 # @File       : __init__.py.py
 # @Author     : GrayZhao
 # @Date       : 2023/7/5 0:01
 # @Version    : 
 # @Description : 
---------------------------------------
"""

from nonebot import on_command, require, get_driver, get_bot
from nonebot.rule import T_State, to_me
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, GroupMessageEvent, Message
from .config import Config
from .data_source import get_60sNews

__help_version__ = '0.1.0'
__help_plugin_name__ = "60s"
__usage__ = """每天60秒读懂世界

使用：
/60s|新闻：查看今天的60s新闻
/60s|新闻+设置 小时:分钟：设置60s新闻的推送时间
/60s|新闻+禁用：禁用60s新闻推送"""

driver = get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)
nickname = list(global_config.nickname)[0]
scheduler = require("nonebot_plugin_apscheduler").scheduler
news60s = on_command("60s", aliases={"news", "新闻"}, rule=to_me(), priority=7, block=True)


async def news60s_reminder():
    bot = get_bot()
    news = await get_60sNews()
    for i in config.news60s_reminder_groups:
        msg = f"「{nickname}·60s读懂世界」\n{news}"
        await bot.call_api('send_group_msg', **{'group_id': i, 'message': Message(msg)})


@news60s.handle()
async def news60s_handle_group(bot: Bot, event: GroupMessageEvent, state: T_State):
    news = await get_60sNews()
    msg = f"「{nickname}·60s读懂世界」\n[CQ:at,qq={event.get_user_id()}]\n{news}"
    await news60s.finish(Message(msg))


@news60s.handle()
async def news60s_handle_private(bot: Bot, event: PrivateMessageEvent, state: T_State):
    news = await get_60sNews()
    msg = f"「{nickname}·60s读懂世界」\n{news}"
    await news60s.finish(Message(msg))


@driver.on_startup
async def _():
    if config.news60s_reminder_start:
        for i in range(len(config.news60s_reminder_time)):
            temp = config.news60s_reminder_time[i].split(":")
            hour = int(temp[0])
            minute = int(temp[1])
            scheduler.add_job(news60s_reminder, 'cron', hour=hour, minute=minute, id=f"news60s_reminder_{i}")
