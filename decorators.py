# -*- coding: utf-8 -*-
# @Time    : 2022/8/31 19:33
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: decorators.py
# @Software: PyCharm
from flask import g, redirect, url_for, flash
from functools import wraps


def login_required(func):
    @wraps(func)  # 使用wraps装饰器保证函数名不因装饰器发生变化，进而保证url_for的正常使用
    def wrapper(*args, **kwargs):
        if hasattr(g, "user"):
            return func(*args, **kwargs)
        flash("请先登录再操作!")
        return redirect(url_for("user.login"))
    return wrapper
