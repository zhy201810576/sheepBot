from nonebot import on_command, get_driver, get_bot
from nonebot.rule import T_State, to_me
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg, ArgPlainText
from nonebot.matcher import Matcher
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, GroupMessageEvent, Message
from .config import Config
from .data_source import get_sorted


__plugin_meta__ = PluginMetadata(
    name="垃圾分类",
    description="垃圾分类小助手，帮助你快速分类垃圾",
    usage="垃圾分类小助手 - 使用：/垃圾|垃圾分类 物品名称",
    config=Config,
    extra={
        "version": '0.1.0'
    },
)


driver = get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)
nickname = list(global_config.nickname)[0]
waste = on_command("垃圾", aliases={"waste", "垃圾分类"}, rule=to_me(), priority=7, block=True)


# @waste.handle()
# async def waste_handle_group(bot: Bot, event: GroupMessageEvent, state: T_State, args: Message = CommandArg()):
#     if name := args.extract_plain_text():
#         text = await get_sorted(name)
#         msg = f"「{nickname}·垃圾分类」\n[CQ:at,qq={event.get_user_id()}]\n{text}"
#         await waste.finish(Message(msg))


@waste.handle()
async def waste_handle_group(event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("name", args)


@waste.got("name", prompt="请输入需要查询分类的物品名称")
async def waste_got_group(bot: Bot, event: GroupMessageEvent, state: T_State, name: str = ArgPlainText()):
    text = await get_sorted(name)
    msg = f"「{nickname}·垃圾分类」\n[CQ:at,qq={event.get_user_id()}]\n{text}"
    await waste.finish(Message(msg))


@waste.handle()
async def waste_handle_private(event: PrivateMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("name", args)


@waste.got("name", prompt="请输入需要查询分类的物品名称")
async def waste_got_private(bot: Bot, event: PrivateMessageEvent, state: T_State, name: str = ArgPlainText()):
    text = await get_sorted(name)
    msg = f"「{nickname}·垃圾分类」\n{text}"
    await waste.finish(Message(msg))
