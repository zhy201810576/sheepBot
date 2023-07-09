from nonebot import on_command, require, get_driver, get_bot
from nonebot.rule import T_State, to_me
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, GroupMessageEvent, Message
from .config import Config
from .data_source import get_moyu


__plugin_meta__ = PluginMetadata(
    name="摸鱼人日历",
    description="发送一幅摸鱼人日历",
    usage="摸鱼人日历 - 使用：/摸鱼|moyu",
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
moyu = on_command("摸鱼", aliases={"moyu", "摸鱼人日历"}, rule=to_me(), priority=7, block=True)


async def moyu_reminder():
    bot = get_bot()
    text = await get_moyu()
    for i in config.moyu_reminder_groups:
        msg = f"「{nickname}·摸鱼人日历」\n{text}"
        await bot.call_api('send_group_msg', **{'group_id': i, 'message': Message(msg)})


@moyu.handle()
async def moyu_handle_group(bot: Bot, event: GroupMessageEvent, state: T_State):
    text = await get_moyu()
    msg = f"「{nickname}·摸鱼人日历」\n[CQ:at,qq={event.get_user_id()}]\n{text}"
    await moyu.finish(Message(msg))


@moyu.handle()
async def moyu_handle_private(bot: Bot, event: PrivateMessageEvent, state: T_State):
    text = await get_moyu()
    msg = f"「{nickname}·摸鱼人日历」\n{text}"
    await moyu.finish(Message(msg))


@driver.on_startup
async def _():
    if config.moyu_reminder_start:
        for i in range(len(config.moyu_reminder_time)):
            temp = config.moyu_reminder_time[i].split(":")
            hour = int(temp[0])
            minute = int(temp[1])
            scheduler.add_job(moyu_reminder, 'cron', hour=hour, minute=minute, id=f"moyu_reminder_{i}")
            logger.debug(f"定时启动,ID:moyu_reminder_{i}, 定时->{hour}:{minute}")
