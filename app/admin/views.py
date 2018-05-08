#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: hanxx
# @Date  : 2018/5/3
# @Desc  : 后端视图

from . import admin
from flask import render_template, redirect, url_for, session, flash, request
# 引入表单验证
from app.admin.forms import LoginForm, TagForm
# 引入数据类型
from app.modules import Admin, Tag
# 引入登陆装饰器
from functools import wraps
# 导入数据库
from app import db


# 登陆装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 主页
@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")


# 管理员登陆
@admin.route("/login/", methods=['GET', 'POST'])
def login():
    # 传入到form
    form = LoginForm()
    # 提交验证
    if form.validate_on_submit():
        # 用户输入数据
        data = form.data
        # 获取数据库账号
        admin = Admin.query.filter_by(name=data['account']).first()
        if admin == None:
            flash("您输入的账号不存在", "err")
            return redirect(url_for("admin.login"))
        if not admin.check_pwd(data['pwd']):
            flash("您输入的密码错误", "err")
            return redirect(url_for("admin.login"))
        # 绑定session
        session['admin'] = data['account']
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


# 管理员退出
@admin.route("/logout/")
@admin_login_req
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))


# 修改密码
@admin.route("/pwd/")
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")


# 添加标签
@admin.route("/tag/add/", methods=['GET', 'POST'])
@admin_login_req
def tag_add():
    # 导入form
    form = TagForm()
    if form.validate_on_submit():
        # 获取页面数据
        data = form.data
        # 查找名称看是否存在
        tag = Tag.query.filter_by(name=data["name"]).count()
        if tag != 0:
            flash("您要添加的标签名称已存在", "err")
            return redirect(url_for('admin.tag_add'))
        # 获取前段数据绑定到ORM中
        tag = Tag(
            name=data["name"]
        )
        # 添加数据库
        db.session.add(tag)
        db.session.commit()
        flash("新增标签成功", "ok")
    return render_template("admin/tag_add.html", form=form)


# 标签列表
@admin.route("/tag/list/<int:page>/", methods=["GET"])
@admin_login_req
def tag_list(page=None):
    '''分页查询'''
    if page is None:
        page = 1
    # paginate page 参数为页码 per_page为每页页数
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)


# 添加电影
@admin.route("/movie/add/")
@admin_login_req
def movie_add():
    return render_template("admin/movie_add.html")


# 电影列表
@admin.route("/movie/list/")
@admin_login_req
def movie_list():
    return render_template("admin/movie_list.html")


# 添加预告
@admin.route("/preview/add/")
@admin_login_req
def preview_add():
    return render_template("admin/preview_add.html")


# 预告列表
@admin.route("/preview/list/")
@admin_login_req
def preview_list():
    return render_template("admin/preview_list.html")


# 用户管理
@admin.route("/user/list/")
@admin_login_req
def user_list():
    return render_template("admin/user_list.html")


# 用户详细信息
@admin.route("/user/view/")
@admin_login_req
def user_view():
    return render_template("admin/user_view.html")


# 评论列表
@admin.route("/comment/list/")
@admin_login_req
def comment_list():
    return render_template("admin/comment_list.html")


# 收藏管理
@admin.route("/miviecol/list/")
@admin_login_req
def moviecol_list():
    return render_template("admin/moviecol_list.html")


# 操作日志
@admin.route("/oplog/list/")
@admin_login_req
def oplog_list():
    return render_template("admin/oplog_list.html")


# 管理员登陆日志
@admin.route("/adminlog/list/")
@admin_login_req
def adminlog_list():
    return render_template("admin/adminlog_list.html")


# 用户登陆日志
@admin.route("/userlog/list/")
@admin_login_req
def userlog_list():
    return render_template("admin/userlog_list.html")


# 添加角色
@admin.route("/role/add/")
@admin_login_req
def role_add():
    return render_template("admin/role_add.html")


# 角色列表
@admin.route("/role/list/")
@admin_login_req
def role_list():
    return render_template("admin/role_list.html")


# 添加权限
@admin.route("/auth/add/")
@admin_login_req
def auth_add():
    return render_template("admin/auth_add.html")


# 权限列表
@admin.route("/auth/list/")
@admin_login_req
def auth_list():
    return render_template("admin/auth_list.html")


# 添加管理员
@admin.route("/admin/add/")
@admin_login_req
def admin_add():
    return render_template("admin/admin_add.html")


# 管理员列表
@admin.route("/admin/list/")
@admin_login_req
def admin_list():
    return render_template("admin/admin_list.html")
