# -*- coding: utf-8 -*-
# @Time    : 2022/8/31 19:33
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: decorators.py
# @Software: PyCharm
from flask import g, url_for, flash, request,render_template
from functools import wraps


def login_required(func):
    @wraps(func)  # 使用wraps装饰器保证函数名不因装饰器发生变化，进而保证url_for的正常使用
    def wrapper(*args, **kwargs):
        before_url = request.url
        if "submit_answer" in before_url:
            before_url = f"/question/{kwargs.get('question_id')}"
        if hasattr(g, "user"):
            return func(*args, **kwargs)
        print("before_url",before_url)
        flash("请先登录再操作!")
        return render_template("login.html", next_url=before_url)
    return wrapper
