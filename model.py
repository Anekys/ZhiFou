# -*- coding: utf-8 -*-
# @Time    : 2022/8/31 9:21
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: model.py
# @Software: PyCharm
from exts import db
from datetime import datetime

class EmailCaptChaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100),nullable=True)
    password = db.Column(db.String(200), nullable=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

class QuestionModel(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20),nullable=True)
    content = db.Column(db.String(256))
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    author = db.relationship(UserModel,backref="questions")


class AnswerModel(db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(256),nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey("questions.id"))
    question = db.relationship(QuestionModel,backref="answers")
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref="answers")