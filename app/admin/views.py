#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: hanxx
# @Date  : 2018/5/3
# @Desc  : 后端视图

from . import admin
from flask import render_template, redirect, url_for, session, flash, request
# 引入表单验证
from app.admin.forms import LoginForm, TagForm, MovieForm
# 引入数据类型
from app.modules import Admin, Tag, Movie
# 引入登陆装饰器
from functools import wraps
# 导入数据库
from app import db, app
# 对文件的操作
import os, datetime, uuid
# 文件名的安全性
from werkzeug.utils import secure_filename


# 登陆装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
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
    '''分页查询标签'''
    if page is None:
        page = 1
    # paginate page 参数为页码 per_page为每页页数
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)


# 删除标签
@admin.route("/tag/del/<int:id>/", methods=["GET"])
@admin_login_req
def tag_del(id=None):
    '''删除标签'''
    # 根据ID查询删除的标签
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    # 闪现消息
    flash('删除"%s"标签成功' % tag.name, "ok")
    return redirect(url_for('admin.tag_list', page=1))


# 编辑标签
@admin.route("/tag/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def tag_edit(id):
    # 导入form
    form = TagForm()
    # 获取需要修改的tag
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        # 获取页面数据
        data = form.data
        # 查找名称看是否存在
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        # 判断是否修改了名称并验证是否重复
        if tag.name != data['name'] and tag_count != 0:
            flash("修改的标签名称已存在", "err")
            return redirect(url_for('admin.tag_edit', id=id))
        # 获取前段数据绑定到ORM中
        tag.name = data['name']
        # 添加数据库
        db.session.add(tag)
        db.session.commit()
        flash("修改标签名称成功", "ok")
    return render_template("admin/tag_edit.html", form=form, tag=tag)


# 添加电影
@admin.route("/movie/add/", methods=['GET', 'POST'])
@admin_login_req
def movie_add():
    form = MovieForm()
    # 上传电影操作
    if form.validate_on_submit():
        # 获取表单数据
        data = form.data
        # 查找电影看是否存在
        movie = Movie.query.filter_by(title=data["title"]).count()
        if movie != 0:
            flash("您要添加的电影已存在库中", "err")
            return redirect(url_for('admin.movie_add'))
        # 如果库中不存在电影则添加
        # 对上传文件进行处理
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        # 上传路径是否存在
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])  # 创建文件目录
            os.chmod(app.config['UP_DIR'], 'rw')  # 读写权限
        # 改名
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        # 保存
        form.url.data.save(app.config['UP_DIR'] + url)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        movie = Movie(
            title=data["title"],
            url=url,  # 文件类型
            info=data['info'],
            logo=logo,  # 文件类型
            star=int(data["star"]),  # 星级需要转换int
            playnum=0,
            commentnum=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']
        )
        # 保存数据库
        db.session.add(movie)
        db.session.commit()
        flash("添加电影%s成功" % movie.title, "ok")
        return redirect(url_for('admin.movie_add'))
    return render_template("admin/movie_add.html", form=form)


# 分页电影列表
@admin.route("/movie/list/<int:page>/", methods=["GET"])
@admin_login_req
def movie_list(page=None):
    '''分页显示电影列表'''
    if page is None:
        page = 1
    # 从数据库关联查询
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/movie_list.html", page_data=page_data)


# 删除电影
@admin.route("/movie/del/<int:id>/", methods=["GET"])
@admin_login_req
# @admin_auth
def movie_del(id=None):
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    # 删除影片
    os.remove(app.config['UP_DIR'] + movie.url)
    os.remove(app.config['UP_DIR'] + movie.logo)
    flash("删除%s电影成功！" % movie.title, "ok")
    return redirect(url_for('admin.movie_list', page=1))


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
