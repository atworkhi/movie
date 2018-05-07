#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: hanxx
# @Date  : 2018/5/3
# @Desc  ：前端视图

from . import home
from flask import render_template, redirect, url_for


# 主页
@home.route("/")
def index():
    return render_template("home/index.html")


# 轮播图
@home.route("/animation/")
def animation():
    return render_template("home/animation.html")


# 搜索
@home.route("/search/")
def search():
    return render_template("home/search.html")


# 登陆
@home.route("/login/")
def login():
    return render_template("home/login.html")


# 注销
@home.route("/logout/")
def logout():
    return redirect(url_for("home.login"))


# 注册
@home.route("/regist/")
def regist():
    return render_template("home/regist.html")


# 用户中心
@home.route("/user/")
def user():
    return render_template("home/user.html")


# 修改密码
@home.route("/pwd/")
def pwd():
    return render_template("home/pwd.html")


# 评论管理
@home.route("/comments/")
def comments():
    return render_template("home/comments.html")


# 登陆日志
@home.route("/loginlog/")
def loginlog():
    return render_template("home/loginlog.html")


# 电影收藏
@home.route("/moviecol/")
def moviecol():
    return render_template("home/moviecol.html")


# 播放页面
@home.route("/play/")
def play():
    return render_template("home/play.html")
