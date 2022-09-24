# -*- coding: utf-8 -*-
# @Time    : 2022/9/4 19:29
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: get_time.py
# @Software: PyCharm
import datetime


def get_current_week():
    """
    获取本周的周一及周日
    """
    monday, sunday = datetime.date.today(), datetime.date.today()
    one_day = datetime.timedelta(days=1)
    seven_day = datetime.timedelta(days=6)
    while monday.weekday() != 0:
        monday -= one_day
    sunday = monday + seven_day
    return monday, sunday


def get_week():
    """
    :return:返回内容为一个字典,其中key为从当日起向前七天的datetime.date,value均为0
    """
    week = {}
    now_time = datetime.datetime.now()
    week.setdefault(now_time.date(), 0)
    for i in range(1, 7):
        one_day = datetime.timedelta(days=i)
        week.setdefault(now_time.date() - one_day, 0)
    return week
if __name__ == '__main__':
    a,b = get_current_week()
    print(a,b)