from nonebot import on_command, get_driver, get_bot
from nonebot.rule import T_State, to_me
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, GroupMessageEvent, Message
from .config import Config
from .data_source import get_joke


__plugin_meta__ = PluginMetadata(
    name="随机一则笑话",
    description="发送随机一则笑话",
    usage="随机一则笑话 - 使用：/笑话|joke",
    config=Config,
    extra={
        "version": '0.1.0'
    },
)


driver = get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)
nickname = list(global_config.nickname)[0]
joke = on_command("笑话", aliases={"joke", "一则笑话"}, rule=to_me(), priority=7, block=True)


@joke.handle()
async def joke_handle_group(bot: Bot, event: GroupMessageEvent, state: T_State):
    text = await get_joke()
    msg = f"「{nickname}·一则笑话」\n[CQ:at,qq={event.get_user_id()}]\n{text}"
    await joke.finish(Message(msg))


@joke.handle()
async def joke_handle_private(bot: Bot, event: PrivateMessageEvent, state: T_State):
    text = await get_joke()
    msg = f"「{nickname}·一则笑话」\n{text}"
    await joke.finish(Message(msg))
