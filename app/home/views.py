#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: hanxx
# @Date  : 2018/5/3
# @Desc  ：前端视图

from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import *
from app.modules import User
from werkzeug.security import generate_password_hash
from app import db, app
from functools import wraps
import uuid, os, datetime


# 登陆装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名
def change_filename(filename):
    # 对文件名进行分割
    fileinfo = os.path.splitext(filename)
    # 时间搓+ uuid+ 后缀
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


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
@home.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if user is None:
            flash('账号不存在！', 'err')
            return redirect(url_for('home.login'))
        if not user.check_pwd(data['pwd']):
            flash('密码错误!', 'err')
            return redirect(url_for('home.login'))
        session['user'] = user.name
        session['user_id'] = user.id

        # 登陆日志的存放
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.user'))
    return render_template("home/login.html", form=form)


# 注销
@home.route("/logout/")
@user_login_req
def logout():
    session.pop('user', None)
    session.pop("user_id", None)
    return redirect(url_for("home.login"))


# 注册
@home.route("/regist/", methods=['GET', 'POST'])
def regist():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            pwd=generate_password_hash(data['pwd']),
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功！请登陆！', 'ok')
        return redirect(url_for('home.login'))
    return render_template("home/regist.html", form=form)


# 用户中心
@home.route("/user/", methods=['GET', 'POST'])
@user_login_req
def user():
    form = UserinfoForm()
    user = User.query.get(int(session['user_id']))
    # 头像可以为空
    form.face.validators = []
    # 判断是get回显数据
    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    # 提交
    if form.validate_on_submit():
        data = form.data
        face_file = form.face.data.filename
        user_face = user.face
        # 头像存放目录不存在则创建
        if not os.path.exists(app.config['UP_FACES']):
            os.makedirs(app.config['UP_FACES'])
            os.chmod(app.config['UP_FACES'], 'rw')
        # 如果没更换则不必添加
        if face_file != '':
            # 重命名并保存
            user_face = change_filename(face_file)
            form.face.data.save(app.config['UP_FACES'] + user_face)
            # # 删除之前头像
            # if os.path.exists(app.config['UP_FACES'] + user.face):
            #     os.remove(app.config['UP_FACES'] + user.face)
        # 验证用户名 邮箱 手机号 是否已经存在
        name_validata = User.query.filter_by(name=data['name']).count()
        if data['name'] != user.name and name_validata != 0:
            flash('用户账号已存在！', 'err')
            return redirect(url_for('home.user'))

        email_validata = User.query.filter_by(email=data['email']).count()
        if data['email'] != user.email and email_validata != 0:
            flash('邮箱已经存在!', 'err')
            return redirect(url_for('home.user'))

        phone_validata = User.query.filter_by(phone=data['phone']).count()
        if data['phone'] != user.phone and phone_validata != 0:
            flash('手机号码已经存在！', 'err')
            return redirect(url_for('home.user'))

        # 更改数据
        user.name = data['name']
        user.email = data['email']
        user.face = user_face
        user.phone = data['phone']
        user.info = data['info']
        db.session.add(user)
        db.session.commit()
        flash('修改成功！', 'ok')
        return redirect(url_for('home.user'))
    return render_template("home/user.html", form=form, user=user)


# 修改密码
@home.route("/pwd/")
@user_login_req
def pwd():
    return render_template("home/pwd.html")


# 评论管理
@home.route("/comments/")
@user_login_req
def comments():
    return render_template("home/comments.html")


# 登陆日志
@home.route("/loginlog/")
@user_login_req
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
