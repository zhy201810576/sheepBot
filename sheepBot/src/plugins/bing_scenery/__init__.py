from nonebot import on_command, require, get_driver, get_bot
from nonebot.rule import T_State, to_me
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, GroupMessageEvent, Message
from .config import Config
from .data_source import get_bing_image


__plugin_meta__ = PluginMetadata(
    name="必应每日一图",
    description="发送必应每日的一幅美图",
    usage="必应每日一图 - 使用：/必应|每日一图",
    config=Config,
    extra={
        "version": '0.1.0'
    },
)


driver = get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)
nickname = list(global_config.nickname)[0]
scheduler = require("nonebot_plugin_apscheduler").scheduler
bing = on_command("每日一图", aliases={"必应", "bing"}, rule=to_me(), priority=7, block=True)


async def bing_reminder():
    bot = get_bot()
    text = await get_bing_image()
    for i in config.bing_reminder_groups:
        msg = f"「{nickname}·必应每日一图」\n{text}"
        await bot.call_api('send_group_msg', **{'group_id': i, 'message': Message(msg)})


@bing.handle()
async def bing_handle_group(bot: Bot, event: GroupMessageEvent, state: T_State):
    text = await get_bing_image()
    msg = f"「{nickname}·必应每日一图」\n[CQ:at,qq={event.get_user_id()}]\n{text}"
    await bing.finish(Message(msg))


@bing.handle()
async def bing_handle_private(bot: Bot, event: PrivateMessageEvent, state: T_State):
    text = await get_bing_image()
    msg = f"「{nickname}·必应每日一图」\n{text}"
    await bing.finish(Message(msg))


@driver.on_startup
async def _():
    if config.bing_reminder_start:
        for i in range(len(config.bing_reminder_time)):
            temp = config.bing_reminder_time[i].split(":")
            hour = int(temp[0])
            minute = int(temp[1])
            scheduler.add_job(bing_reminder, 'cron', hour=hour, minute=minute, id=f"bing_reminder_{i}")
            logger.debug(f"定时启动,ID:bing_reminder_{i}, 定时->{hour}:{minute}")
