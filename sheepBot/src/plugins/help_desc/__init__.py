from nonebot import on_command, get_driver, get_bot
from nonebot.rule import T_State, to_me
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, GroupMessageEvent, Message
from .config import Config


__plugin_meta__ = PluginMetadata(
    name="命令帮助",
    description="机器人命令帮助",
    usage="命令帮助 - 使用：/帮助|help",
    config=Config,
    extra={
        "version": '0.1.0'
    },
)


driver = get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)
nickname = list(global_config.nickname)[0]
_help = on_command("命令帮助", aliases={"help", "帮助"}, rule=to_me(), priority=7, block=True)
help_text = f"""[CQ:face,id=54] 群聊中需要 <@{nickname}> [CQ:face,id=54]

* 📰 60秒读懂世界
 - 使用：/60s|新闻
* 🖼 必应每日一图
 - 使用：/必应|每日一图
* 📅 摸鱼人日历
 - 使用：/摸鱼|moyu
* ⏲ 历史上的今天
 - 使用：/历史|历史上的今天
* 🤣 随机一则笑话
 - 使用：/笑话|joke
* 🏞 随机一幅风景照
 - 使用：/风景|scenic
* ♻ 垃圾分类小助手
 - 使用：/垃圾|垃圾分类 物品名称
"""


@_help.handle()
async def _help_handle_group(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = f"「{nickname}·命令」\n[CQ:at,qq={event.get_user_id()}]\n{help_text}"
    await _help.finish(Message(msg))


@_help.handle()
async def _help_handle_private(bot: Bot, event: PrivateMessageEvent, state: T_State):
    msg = f"「{nickname}·命令」\n{help_text}"
    await _help.finish(Message(msg))

