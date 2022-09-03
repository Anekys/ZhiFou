# -*- coding: utf-8 -*-
# @Time    : 2022/8/30 11:38
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: qa.py
# @Software: PyCharm
from flask import Blueprint, render_template, request, g, redirect, url_for, flash
from exts import db
from decorators import login_required
from .forms import QuestionForm, AnswerForm
from model import QuestionModel, AnswerModel
from datetime import datetime

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/", methods=["GET", "POST"])
def index():
    questions = QuestionModel.query.order_by(db.text("-create_time")).all()
    return render_template("index.html", questions=questions)


@bp.route("/public_question", methods=["GET", "POST"])
@login_required
def public_question():
    if request.method == "GET":
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            flash("标题不能少于5个字符!")
            return url_for("qa.public_question")


@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    answer = AnswerModel.query.filter_by(question_id=question_id).all()
    return render_template("detail.html", question=question, answers=answer)

@bp.route("/submit_answer/<int:question_id>",methods=["POST"])
@login_required
def submit_answer(question_id):
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        answer = AnswerModel(content=content, question_id=question_id
                             #  给relationship设置值orm框架会自动设置对应的author_id
                             , author=g.user)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.question_detail", question_id=question_id))

    else:
        flash("提交回答的内容最少5个字符,最多256个字符!")
        return redirect(url_for("qa.question_detail", question_id=question_id))
