# -*- coding: utf-8 -*-
# @Time    : 2022/9/9 10:52
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: SpideForZhiHu.py
# @Software: PyCharm
from playwright.sync_api import sync_playwright
from parsel import Selector
import pymysql
from datetime import datetime

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='root',
                     database='zhifou')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def getQuestion():
    p = sync_playwright().start()
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.zhihu.com/knowledge-plan/hot-question/hot/0/hour")
    page.wait_for_load_state('networkidle')
    source = page.content()
    html = Selector(text=source)
    divlist = html.css("div[role=list]").css("div[class=css-vurnku]")
    question_list = []
    for item in divlist:
        title = item.xpath("./div/div[1]/a/div/text()").get()
        if not title:
            continue
        question_list.append(title)
    return question_list


def task(question_list):
    for question_title in question_list:
        cursor.execute(f'SELECT id from questions where title = "{question_title}"')
        data = cursor.fetchone()
        if not data:
            sql = f"""INSERT INTO questions(title,content,author_id, create_time)
                     VALUES ("{question_title}", "{question_title}", 2,"{datetime.now()}")"""
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print("知乎问题插入成功:", question_title)
            except Exception as err:
                # 如果发生错误则回滚
                db.rollback()


def InsertData():
    qlist = getQuestion()
    task(qlist)


if __name__ == '__main__':
    qlist = getQuestion()
    task(qlist)
