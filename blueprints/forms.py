# -*- coding: utf-8 -*-
# @Time    : 2022/8/31 10:26
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: forms.py
# @Software: PyCharm
import wtforms
from wtforms.validators import length, email, EqualTo, InputRequired
from model import EmailCaptChaModel, UserModel


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class RegisterForm(wtforms.Form):
    nickname = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    confirm = wtforms.StringField(validators=[EqualTo("password")])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])

    def validate_captcha(self, field):
        captcha = field.data
        captcha_model = EmailCaptChaModel.query.filter_by(email=self.email.data).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError("邮箱验证码错误!")

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError("用户已经注册!")


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=5, max=20)])
    content = wtforms.StringField(validators=[length(max=256)])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[InputRequired(),length(min=5, max=256)])