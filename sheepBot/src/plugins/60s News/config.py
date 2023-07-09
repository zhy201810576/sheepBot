#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" 
---------------------------------------
 # @Project    : sheepBot
 # @File       : config.py
 # @Author     : GrayZhao
 # @Date       : 2023/7/5 0:03
 # @Version    : 
 # @Description : 
---------------------------------------
"""
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    # 定时提醒开关
    news60s_reminder_start: bool = True

    # 定时提醒推送的群号
    news60s_reminder_groups: list = [""]

    # 定时提醒时间
    news60s_reminder_time: list = ["08:00"]
