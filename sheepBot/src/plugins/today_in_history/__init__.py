from nonebot import on_command, require, get_driver, get_bot
from nonebot.rule import T_State, to_me
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, GroupMessageEvent, Message
from .config import Config
from .data_source import get_today_in_history


__plugin_meta__ = PluginMetadata(
    name="历史上的今天",
    description="发送每日历史上的今天",
    usage="历史上的今天 - 使用：/历史|历史上的今天",
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
history = on_command("历史", aliases={"history", "历史上的今天"}, rule=to_me(), priority=7, block=True)


async def history_reminder():
    bot = get_bot()
    text = await get_today_in_history()
    for i in config.history_reminder_groups:
        msg = f"「{nickname}·历史上的今天」\n{text}"
        await bot.call_api('send_group_msg', **{'group_id': i, 'message': Message(msg)})


@history.handle()
async def history_handle_group(bot: Bot, event: GroupMessageEvent, state: T_State):
    text = await get_today_in_history()
    msg = f"「{nickname}·历史上的今天」\n[CQ:at,qq={event.get_user_id()}]\n{text}"
    await history.finish(Message(msg))


@history.handle()
async def history_handle_private(bot: Bot, event: PrivateMessageEvent, state: T_State):
    text = await get_today_in_history()
    msg = f"「{nickname}·历史上的今天」\n{text}"
    await history.finish(Message(msg))


@driver.on_startup
async def _():
    if config.history_reminder_start:
        for i in range(len(config.history_reminder_time)):
            temp = config.history_reminder_time[i].split(":")
            hour = int(temp[0])
            minute = int(temp[1])
            scheduler.add_job(history_reminder, 'cron', hour=hour, minute=minute, id=f"history_reminder_{i}")
            logger.debug(f"定时启动,ID:history_reminder_{i}, 定时->{hour}:{minute}")
