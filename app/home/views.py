#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: hanxx
# @Date  : 2018/5/3
# @Desc  ：前端视图

from . import home
from flask import render_template, redirect, url_for, flash, session, request, Response
from app.home.forms import *
from app.modules import User
from werkzeug.security import generate_password_hash
from app import db, app, rd
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
@home.route("/<int:page>/", methods=['GET'])
@home.route("/", methods=['GET'])
def index(page=None):
    # 获取所有标签
    tags = Tag.query.all()
    # 分页查询
    page_data = Movie.query
    # 标签筛选
    tid = request.args.get('tid', 0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))

    # 星级筛选
    star = request.args.get('star', 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))

    # 时间排序
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )

    # 播放量
    pm = request.args.get('pm', 0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.playnum.asc()
            )

    # 评论量
    cm = request.args.get('cm', 0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentnum.asc()
            )

    if page is None:
        page = 1

    page_data = page_data.paginate(page=page, per_page=10)
    # 参数放入到字典
    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm,
    )
    page_data.p = p
    return render_template("home/index.html", tags=tags, p=p, page_data=page_data)


# 轮播图
@home.route("/animation/")
def animation():
    data = Preview.query.all()
    return render_template("home/animation.html", data=data)


# 搜索
@home.route("/search/<int:page>/")
def search(page=None):
    if page is None:
        page = 1
    # 搜索的关键字
    key = request.args.get('key', '')
    # 找到多少条记录
    movie_count = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).count()
    page_data = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    # 把关键字传入便于搜索分页
    page_data.key = key
    return render_template("home/search.html", key=key, movie_count=movie_count, page_data=page_data)


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
            print(type(user.face))
            # # 删除之前头像
            if not user.face is None and os.path.exists(app.config['UP_FACES'] + user.face):
                os.remove(app.config['UP_FACES'] + user.face)
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
@home.route("/pwd/", methods=['GET', 'POST'])
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session['user']).first()
        if not user.check_pwd(data['old_pwd']):
            flash('旧密码输入错误！', 'err')
            return redirect(url_for('home.pwd'))
        user.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(user)
        db.session.commit()
        flash('修改密码成功,请重新登陆！', 'ok')
        return redirect(url_for('home.logout'))
    return render_template("home/pwd.html", form=form)


# 评论管理
@home.route("/comments/<int:page>/", methods=['GET'])
@user_login_req
def comments(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        # 只获取登陆账户的评论记录
        User.id == session['user_id'],
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/comments.html", page_data=page_data)


# 登陆日志
@home.route("/loginlog/<int:page>/", methods=['GET'])
@user_login_req
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.filter_by(
        user_id=int(session['user_id'])
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/loginlog.html", page_data=page_data)


# 添加电影的收藏
@home.route("/moviecol/add/", methods=['GET'])
@user_login_req
def moviecol_add():
    # 获取用户与电影
    uid = request.args.get('uid', '')
    mid = request.args.get('mid', '')
    moviecol = Moviecol.query.filter_by(
        user_id=int(uid),
        movie_id=int(mid)
    ).count()
    # 判断是否已经收藏
    if moviecol != 0:
        data = dict(ok=0)
    # 未收藏时进行收藏
    if moviecol == 0:
        moviecol = Moviecol(
            user_id=int(uid),
            movie_id=int(mid),
        )
        db.session.add(moviecol)
        db.session.commit()
        data = dict(ok=1)
    # 返回json
    import json
    return json.dumps(data)


# 电影收藏列表
@home.route("/moviecol/<int:page>/", methods=['GET'])
def moviecol(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(
        User
    ).join(
        Movie
    ).filter(
        User.id == session['user_id'],
        Movie.id == Moviecol.movie_id
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/moviecol.html", page_data=page_data)


# 播放页面
@home.route("/play/<int:id>/<int:page>/", methods=['GET', 'POST'])
def play(id=None, page=None):
    movie = Movie.query.join(
        Tag
    ).filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id)
    ).first_or_404()
    # 播放量+1
    movie.playnum = movie.playnum + 1

    # 获取评论的所有列表
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == movie.id,
        # 获取所有用户的评论
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)

    # 获取评论条数
    count_com = Comment.query.filter_by(
        movie_id=movie.id
    ).count()

    # 提交评论
    form = CommentForm()
    if form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['content'],
            movie_id=movie.id,
            user_id=session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        movie.commentnum = movie.commentnum + 1
        db.session.add(movie)
        db.session.commit()
        flash('添加评论成功', 'ok')
        return redirect(url_for('home.play', id=movie.id, page=1))
    db.session.add(movie)
    db.session.commit()
    return render_template("home/play.html", movie=movie, form=form, page_data=page_data, count_com=count_com)


# 弹幕播放器
@home.route("/video/<int:id>/<int:page>/", methods=['GET', 'POST'])
def video(id=None, page=None):
    movie = Movie.query.join(
        Tag
    ).filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id)
    ).first_or_404()
    # 播放量+1
    movie.playnum = movie.playnum + 1

    # 获取评论的所有列表
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == movie.id,
        # 获取所有用户的评论
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)

    # 获取评论条数
    count_com = Comment.query.filter_by(
        movie_id=movie.id
    ).count()

    # 提交评论
    form = CommentForm()
    if form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['content'],
            movie_id=movie.id,
            user_id=session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        movie.commentnum = movie.commentnum + 1
        db.session.add(movie)
        db.session.commit()
        flash('添加评论成功', 'ok')
        return redirect(url_for('home.video', id=movie.id, page=1))
    db.session.add(movie)
    db.session.commit()
    return render_template("home/video.html", movie=movie, form=form, page_data=page_data, count_com=count_com)


# 添加弹幕
@home.route("/tm/", methods=["GET", "POST"])
def tm():
    import json
    if request.method == "GET":
        # 获取弹幕消息队列
        id = request.args.get('id')
        key = "movie" + str(id)
        if rd.llen(key):
            msgs = rd.lrange(key, 0, 2999)
            res = {
                "code": 1,
                "danmaku": [json.loads(v) for v in msgs]
            }
        else:
            res = {
                "code": 1,
                "danmaku": []
            }
        resp = json.dumps(res)
    if request.method == "POST":
        # 添加弹幕
        data = json.loads(request.get_data())
        msg = {
            "__v": 0,
            "author": data["author"],
            "time": data["time"],
            "text": data["text"],
            "color": data["color"],
            "type": data['type'],
            "ip": request.remote_addr,
            "_id": datetime.datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex,
            "player": [
                data["player"]
            ]
        }
        res = {
            "code": 1,
            "data": msg
        }
        resp = json.dumps(res)
        rd.lpush("movie" + str(data["player"]), json.dumps(msg))
    return Response(resp, mimetype='application/json')
