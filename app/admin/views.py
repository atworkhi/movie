#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: hanxx
# @Date  : 2018/5/3
# @Desc  : 后端视图

from . import admin
from flask import render_template, redirect, url_for

# 主页
@admin.route("/")
def index():
    return render_template("admin/index.html")


# 管理员登陆
@admin.route("/login/")
def login():
    return render_template("admin/login.html")


# 管理员退出
@admin.route("/logout/")
def logout():
    return redirect(url_for("admin.login"))

# 修改密码
@admin.route("/pwd/")
def pwd():
    return render_template("admin/pwd.html")