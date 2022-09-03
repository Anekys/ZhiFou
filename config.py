# -*- coding: utf-8 -*-
# @Time    : 2022/8/29 20:03
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: config.py
# @Software: PyCharm


# MySQL连接配置
JSON_AS_ASCII = False
DEBUG = True
USERNAME = "root"
PASSWORD = "root"
HOSTNAME = "127.0.0.1"
PORT = 3306
DATABASE = "zhifou"
URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
SQLALCHEMY_DATABASE_URI = URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "zhifouZhiFou"

# Mail服务器配置
MAIL_SERVER = 'smtp.163.com'
MAIL_PROT = 465
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "Anekys@163.com"
MAIL_PASSWORD = "IPXACPUHXMBQMVOF"
MAIL_DEBUG = True
MAIL_DEFAULT_SENDER = ("知否","Anekys@163.com")
