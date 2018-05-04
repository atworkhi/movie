#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: hanxx
# @Date  : 2018/5/3
# @Desc  ：前端视图

from . import home
from flask import render_template,redirect,url_for


# 主页
@home.route("/")
def index():
    return render_template("home/index.html")

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