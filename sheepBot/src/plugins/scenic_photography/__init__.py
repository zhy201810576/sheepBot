from nonebot import on_command, get_driver, get_bot
from nonebot.rule import T_State, to_me
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, GroupMessageEvent, Message
from .config import Config
from .data_source import get_photo


__plugin_meta__ = PluginMetadata(
    name="随机一幅风景照",
    description="发送随机一幅风景照",
    usage="随机一幅风景照 - 使用：/风景|scenic",
    config=Config,
    extra={
        "version": '0.1.0'
    },
)


driver = get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)
nickname = list(global_config.nickname)[0]
scenic = on_command("风景", aliases={"scenic", "风景照"}, rule=to_me(), priority=7, block=True)


@scenic.handle()
async def scenic_handle_group(bot: Bot, event: GroupMessageEvent, state: T_State):
    text = await get_photo()
    msg = f"「{nickname}·风景照」\n[CQ:at,qq={event.get_user_id()}]\n{text}"
    await scenic.finish(Message(msg))


@scenic.handle()
async def scenic_handle_private(bot: Bot, event: PrivateMessageEvent, state: T_State):
    text = await get_photo()
    msg = f"「{nickname}·风景照」\n{text}"
    await scenic.finish(Message(msg))
