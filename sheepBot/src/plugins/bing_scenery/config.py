from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    # 定时提醒开关
    bing_reminder_start: bool = True

    # 定时提醒推送的群号
    bing_reminder_groups: list = [""]

    # 定时提醒时间
    bing_reminder_time: list = ["08:02"]
