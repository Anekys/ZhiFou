# -*- coding: utf-8 -*-
# @Time    : 2022/8/30 11:35
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: user.py
# @Software: PyCharm
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify,flash,g
from exts import mail, db
from flask_mail import Message
from model import EmailCaptChaModel, UserModel
import string, random
from datetime import datetime
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    loginform = LoginForm(request.form)
    if loginform:
        email = request.form.get("email")
        password = request.form.get("password")
        user = UserModel.query.filter_by(email=email).first()
        next_url = request.form.get("next_url")
        if not user:
            flash("用户不存在!")
            return redirect(url_for("user.login"))
        if check_password_hash(user.password, password):
            session["uid"] = user.id
            print(f"{user.nickname}已登录")
            if next_url:
                print("即将跳转到",next_url)
                return redirect(next_url)
            else:
                return redirect("/")
        flash("用户名或密码错误!")
        return redirect(url_for("user.login"))
    flash("用户名或密码格式不正确!")
    return redirect(url_for("user.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    form = RegisterForm(request.form)
    if form.validate():
        email = form.email.data
        nickname = form.nickname.data
        password = form.password.data
        hash_password = generate_password_hash(password)
        user = UserModel(email=email, nickname=nickname, password=hash_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user.login"))
    else:
        session["message"] = "注册失败,提交内容格式错误"
        return redirect(url_for("user.register"))


@bp.route("/get_captcha", methods=["POST"])
def get_captcha():
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    email = request.form.get("email")
    if not email:
        return jsonify({
            "stats": 400,
            "message": "请输入邮箱地址"
        })
    message = Message(
        subject="知否验证码",
        recipients=[email, ],
        body=f"【知否】您正在注册知否账户,注册验证码是:{captcha}.为了您的个人信息安全,请不要将验证码告诉任何人！",
    )
    mail.send(message)
    captcha_model = EmailCaptChaModel.query.filter_by(email=email).first()
    if captcha_model:
        captcha_model.captcha = captcha
        captcha_model.create_time = datetime.now()
        db.session.commit()
    else:
        captcha_model = EmailCaptChaModel(email=email, captcha=captcha)
        db.session.add(captcha_model)
        db.session.commit()
    print(f"{email}的验证码为 ---> {captcha}")
    return jsonify({
        "stats": 200,
        "message": "验证码发送成功"
    })

@bp.route("/logout")
def logout():
    session.clear()
    # g.pop("user")
    return redirect("/")