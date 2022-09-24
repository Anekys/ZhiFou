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
from utils.get_time import get_week
from utils.word_tools import count_from_str, generate_png, cut_words
import os

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/", methods=["GET"])
def index():
    # questions = QuestionModel.query.order_by(QuestionModel.id.desc()).limit(4).offset(0).all()
    return redirect(url_for("qa.next_page", pageIndex=1))


@bp.route("/page/<int:pageIndex>")
def next_page(pageIndex):
    pageSize = 3
    paginate = QuestionModel.query.order_by(db.text("-create_time")).paginate(pageIndex, pageSize, error_out=False)
    stus = paginate.items
    return render_template("index.html", paginate=paginate, questions=stus)


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
    page = int(request.args.get('page', 1))
    pageSize = 5
    paginate = AnswerModel.query.order_by(db.text("-create_time")).filter_by(question_id=question_id).paginate(page,
                                                                                                               pageSize,
                                                                                                               error_out=False)
    answer = paginate.items
    return render_template("detail.html", question=question, answers=answer, paginate=paginate)


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
    page = int(request.args.get('page', 1))
    pageSize = 3
    words = request.args.get("words")
    paginates = QuestionModel.query.filter(QuestionModel.title.like(f'%{words}%'))
    if paginates == []:
        paginates = QuestionModel.query.filter(QuestionModel.content.like(f"%{words}%"))
        if paginates == []:
            paginates = QuestionModel.query.join(UserModel).filter(UserModel.nickname.like(f"%{words}%"))
    paginates = paginates.paginate(page, pageSize, error_out=False)
    questions = paginates.items
    return render_template("result.html", questions=questions, paginate=paginates)


@bp.route("/mine_question")
@login_required
def mine_question():
    page = int(request.args.get('page', 1))
    pageSize = 3
    paginate = QuestionModel.query.filter_by(author=g.user).paginate(page, pageSize, error_out=False)
    questions = paginate.items
    return render_template("mine.html", questions=questions, paginate=paginate)


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


@bp.route("/pie_chart", methods=["GET", "POST"])
@login_required
def pie_chart():
    if request.method == "GET":
        return render_template("pie_chart.html")
    questions = QuestionModel.query.filter_by(author=g.user).all()
    title_str = ""
    for question in questions:
        title_str += question.title
    result = count_from_str(title_str)
    return jsonify({
        "data":result
    })


@bp.route("/wordcloud",methods=["GET"])
@login_required
def wordcloud():
    questions = QuestionModel.query.filter_by(author=g.user).all()
    title_str = ""
    for question in questions:
        title_str += question.title
    result = cut_words(title_str)
    generate_png(result)
    return render_template("wordcloud.html")