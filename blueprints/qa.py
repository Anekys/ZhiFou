# -*- coding: utf-8 -*-
# @Time    : 2022/8/30 11:38
# @Author  : Ane
# @email   : upapqqxyz@gmail.com
# @FileName: qa.py
# @Software: PyCharm
from flask import Blueprint, render_template, request, g, redirect, url_for, flash, jsonify
from exts import db
from decorators import login_required
from .forms import QuestionForm, AnswerForm
from model import QuestionModel, AnswerModel, UserModel
from utils.sort import sort_answer_by_time_desc
from utils.get_time import get_week

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
            flash("标题应大于5个字小于20个字,描述不能超过256字")
            return redirect(url_for("qa.public_question"))


@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    answer = AnswerModel.query.filter_by(question_id=question_id).all()
    sort_answer_by_time_desc(answer)
    return render_template("detail.html", question=question, answers=answer)


@bp.route("/submit_answer/<int:question_id>", methods=["POST"])
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


@bp.route("/search", methods=["GET"])
def question_search():
    words = request.args.get("words")
    questions = QuestionModel.query.filter(QuestionModel.title.like(f'%{words}%')).all()
    if questions == []:
        questions = QuestionModel.query.filter(QuestionModel.content.like(f"%{words}%")).all()
        if questions == []:
            questions = QuestionModel.query.join(UserModel).filter(UserModel.nickname.like(f"%{words}%")).all()
    return render_template("result.html", questions=questions)


@bp.route("/mine_question")
@login_required
def mine_question():
    questions = QuestionModel.query.filter_by(author=g.user).all()
    return render_template("mine.html", questions=questions)


@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def mine_dashboard():
    if request.method == "GET":
        return render_template("date_charts.html")
    questions = QuestionModel.query.filter_by(author=g.user).all()
    week_data = get_week()
    for question in questions:
        create_time = question.create_time.date()
        if create_time in week_data:
            week_data[create_time] += 1
    date = [str(i) for i in week_data.keys()]
    data = [i for i in week_data.values()]
    return jsonify({
        "week_date": date,
        "week_data": data
    })
