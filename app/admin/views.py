#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: hanxx
# @Date  : 2018/5/3
# @Desc  : 后端视图

from . import admin
from flask import render_template, redirect, url_for, session, flash, request
# 引入表单验证
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm, PwdForm
# 引入数据类型
from app.modules import Admin, Tag, Movie, Preview, User, Comment, Moviecol
# 引入登陆装饰器
from functools import wraps
# 导入数据库
from app import db, app
# 对文件的操作
import os, datetime, uuid
# 文件名的安全性 不支持中文格式的文件名
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
    session.pop('admin', None)
    session.pop('admin_id', None)
    return redirect(url_for("admin.login"))


# 修改密码
@admin.route("/pwd/", methods=['GET', 'POST'])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data=form.data
        admin = Admin.query.filter_by(name=session['admin']).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(admin)
        db.session.commit()
        flash('修改密码成功！请重新登陆！', 'ok')
        return redirect(url_for('admin.logout'))
    return render_template("admin/pwd.html", form=form)


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
        file_url = form.url.data.filename
        # print(file_url)
        file_logo = form.logo.data.filename
        # print(file_logo)
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
            tag_id=int("tag_id"),
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
def movie_del(id=None):
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    # 删除影片
    os.remove(app.config['UP_DIR'] + movie.url)
    os.remove(app.config['UP_DIR'] + movie.logo)
    flash("删除%s电影成功！" % movie.title, "ok")
    return redirect(url_for('admin.movie_list', page=1))


# 编辑电影
@admin.route("/movie/edit/<int:id>/", methods=['GET', 'POST'])
@admin_login_req
def movie_edit(id=None):
    form = MovieForm()
    form.url.validators = []
    form.logo.validators = []
    # 根据id查询需要修改的数据
    movie = Movie.query.get_or_404(id)
    # 判断是什么GET请求进行回显下拉选择
    if request.method == "GET":
        form.info.data = movie.info  # 对文本域进行赋值
        form.tag_id.data = movie.tag_id  # 对下拉框回显
        form.star.data = movie.star  # 对下拉框回显
    if form.validate_on_submit():
        data = form.data
        # 判断需要修改的片名是否存在
        movie_count = Movie.query.filter_by(title=data["title"]).count()
        if movie_count != 0 and movie.title != data['title']:
            flash("片名已存在！", 'err')
            return redirect(url_for('admin.movie_edit', id=id))
        # 修改片名与封面
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        if form.url.data != "":
            os.remove(app.config['UP_DIR'] + movie.url)
            file_url = form.url.data.filename
            movie.url = change_filename(file_url)
            form.url.data.save(app.config["UP_DIR"] + movie.url)
        if form.logo.data != "":
            os.remove(app.config['UP_DIR'] + movie.logo)
            file_logo = form.logo.data.filename
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + movie.logo)
        # 修改的数据
        movie.star = data['star']
        movie.tag_id = data['tag_id']
        movie.info = data["info"]
        movie.title = data["title"]
        movie.area = data["area"]
        movie.length = data["length"]
        movie.release_time = data["release_time"]
        db.session.add(movie)
        db.session.commit()
        flash("修改电影成功", "ok")
        return redirect(url_for("admin.movie_edit", id=movie.id))
    # movie = movie 为给前台赋值
    return render_template("admin/movie_edit.html", form=form, movie=movie)


# 添加预告
@admin.route("/preview/add/", methods=['GET', 'POST'])
@admin_login_req
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        # 验证电影预告是否已经存在
        preview = Preview.query.filter_by(title=data["title"]).count()
        if preview != 0:
            flash("您要添加的电影预告已存在", "err")
            return redirect(url_for('admin.preview_add'))
        # 如果不存在在添加 其中涉及文件上传
        file_logo = form.logo.data.filename
        # 判断上传路径是否存在
        if not os.path.exists(app.config['UP_PREVIEW']):
            os.makedirs(app.config['UP_PREVIEW'])
            os.chmod(app.config['UP_PREVIEW'], 'rw')
        # 改名进行上传
        logo = change_filename(file_logo)
        # 上传
        form.logo.data.save(app.config['UP_PREVIEW'] + logo)
        preview = Preview(
            title=data['title'],
            logo=logo
        )
        # 保存数据库
        db.session.add(preview)
        db.session.commit()
        flash("添加电影预告%s成功" % preview.title, 'ok')
        return redirect(url_for('admin.preview_add'))
    return render_template("admin/preview_add.html", form=form)


# 预告列表
@admin.route("/preview/list/<int:page>/", methods=['GET'])
@admin_login_req
def preview_list(page=None):
    '''电影预告展示列表'''
    if page is None:
        page = 1
    # paginate page 参数为页码 per_page为每页页数
    page_data = Preview.query.order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/preview_list.html", page_data=page_data)


# 删除预告
@admin.route("/preview/del/<int:id>/", methods=['GET'])
@admin_login_req
def preview_del(id=None):
    if id is None:
        flash("未发现此电影预告", "err")
        return redirect(url_for('admin.preview_list', page=1))
    # 删除
    preview = Preview.query.get_or_404(int(id))
    db.session.delete(preview)
    db.session.commit()
    # 删除文件
    os.remove(app.config['UP_PREVIEW'] + preview.logo)
    # 闪现消息
    flash('删除%s预告成功' % preview.title, "ok")
    return redirect(url_for('admin.preview_list', page=1))


# 编辑预告
@admin.route("/preview/edit/<int:id>/", methods=['GET', 'POST'])
@admin_login_req
def preview_edit(id):
    '''编辑'''
    form = PreviewForm()
    form.logo.validators = []
    # 根据ID查找数据并回显
    preview = Preview.query.get_or_404(int(id))
    if form.validate_on_submit():
        data = form.data
        preview_count = Preview.query.filter_by(title=data["title"]).count()
        if preview_count != 0 and preview.title != data['title']:
            flash("你要修改的预告名称已存在", "err")
            return redirect(url_for('admin.preview_edit', id=id))
        # 修改logo
        if form.logo.data != '':
            os.remove(app.config['UP_PREVIEW'] + preview.logo)
            file_logo = form.logo.data.filename
            # 把logo存入数据库
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_PREVIEW'] + preview.logo)
        # 修改数据
        preview.title = data['title']
        db.session.add(preview)
        db.session.commit()
        flash("修改预告成功", "ok")
        return redirect(url_for("admin.preview_edit", id=preview.id))
    # movie = movie 为给前台赋值
    return render_template("admin/preview_edit.html", form=form, preview=preview)


# 用户管理
@admin.route("/user/list/<int:page>/", methods=['GET'])
@admin_login_req
def user_list(page=None):
    '''用户列表'''
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/user_list.html", page_data=page_data)


# 用户详细信息
@admin.route("/user/view/<int:id>/", methods=['GET'])
@admin_login_req
def user_view(id=None):
    '''查看详细信息'''
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html", user=user)


# 删除用户信息
@admin.route("/user/del/<int:id>/", methods=['GET'])
@admin_login_req
def user_del(id=None):
    if id is None:
        flash("未发现要删除的用户", 'err')
        return redirect(url_for('admin.user_list', page=1))
    # 查找数据库
    user = User.query.get_or_404(int(id))
    # 删除数据库
    db.session.delete(user)
    db.session.commit()
    # 删除头像文件
    os.remove(app.config['UP_FACES'] + user.face)
    # 闪现消息
    flash('删除%s用户成功' % user.name, 'ok')
    return redirect(url_for('admin.user_list', page=1))


# 评论列表
@admin.route("/comment/list/<int:page>/", methods=['GET'])
@admin_login_req
def comment_list(page=None):
    # 查询评论列表
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/comment_list.html", page_data=page_data)


# 删除评论
@admin.route("/comment/del/<int:id>/", methods=['GET'])
@admin_login_req
def comment_del(id=None):
    comment = Comment.query.get_or_404(int(id))
    db.session.delete(comment)
    db.session.commit()
    flash('删除评论成功', 'ok')
    return redirect(url_for('admin.comment_list', page=1))


# 收藏管理
@admin.route("/miviecol/list/<int:page>/", methods=['GET'])
@admin_login_req
def moviecol_list(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/moviecol_list.html", page_data=page_data)


# 删除收藏
@admin.route("/moviecol/del/<int:id>/", methods=['GET'])
@admin_login_req
def moviecol_del(id=None):
    moviecol = Moviecol.query.get_or_404(int(id))
    db.session.delete(moviecol)
    db.session.commit()
    flash('删除用户收藏电影', 'ok')
    return redirect(url_for('admin.moviecol_list', page=1))


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
