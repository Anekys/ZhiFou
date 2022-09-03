# -*- coding: utf-8 -*-
# @Time    : 2022/8/30 11:33
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: exts.py
# @Software: PyCharm

# 加载数据库框架
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# 加载邮箱框架
from flask_mail import Mail
mail = Mail()