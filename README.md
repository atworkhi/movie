## flask web 框架的使用
#### 环境的搭建：
+  使用虚拟化环境：virtualenv
 安装virtualenv
> pip install virtualenv

创建虚拟目录：
> cd my_project_dir

> virtualenv venv #venv为虚拟环境目录名，目录名自定义

激活虚拟环境：
> source venv/bin/activate

退出虚拟环境：
> deactivate

+ 使用pycharm创建flask项目

#### 文件目录：
```text
 manage.py      入口启动脚本
 app            项目目录
 __init__.py    初始化文件
 models.py      数据模型文件
 static         静态资源文件
 home/admin     前后台模块
 views.py       视图处理文件
 forms.py       表单处理文件
 templates      模版目录
```
#### 蓝图构建项目目录  blueprint
```text
它的主要功能是使模块式开发成为可能。
```
编辑蓝图
```text
form flask import Blueprint
admin = Blueprint("admin",__name__)
import views
```
注册蓝图
```text
form admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint,url_prefix = "/admin")
```
调用蓝图
```text
from . import admin
@admin.route("/")
```
#### 数据库ORM  flask-sqlalchemy
安装：
> pip install flask-sqlalchemy

链接：
```text
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://账号:密码@127.0.0.1:3306/数据库"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
```
##### 引入资源文件与前端页面：
> 说明：静态文件在static目录下，页面放在 templates

引入模板
> from flask import Flask,render_template

引入静态资源文件：
> href="{{ url_for('static',filename='路径')}}

返回页面：
> return render_template('xxx.html')
```
静态文件引入： {{url_for('static',filename='文件路径')}}
定义路由：{{url_for(’模块名.视图名‘，变量=参数)}}
定义数据块：{% block 数据块名称 %}... {% endblock%}
```
##### 登陆页面的搭建：
```
@home.route("/login/")  登陆
from flask import render_template,redirect,url_for
@home.route("/logout/") 注销 -- 重定向
@home.route("/regist/") 注册

继承公共页面
{% extends "home/home.html" %}
在代码块中填入单独的央视
{% block content %}
{% endblock %}
```
##### 用户详情与用户页面的搭建：
会员中心 修改密码 评论管理 登陆日志 电影收藏
```
{% include "home/menu.html" %} 包含页面
```
##### 首页的搭建：
{% for v in range(1,13) %} for 语法使用 与轮播图的实现

##### 搜索页面：
##### 播放页面：
##### 后台管理页面：
```
登陆-login 退出-logout 父模版-admin 导航页面-nav 修改密码-pwd
控制面板-index 标签页面/添加-tag 影视管理-movie 幕布推荐-preview
会员管理-user 评论管理-comment 收藏管理-moviecol
操作日志-oplog 管理员日志-adminlog 会员登陆日志-userlog
角色管理-role  权限管理-auth 管理员-admin
```
### 后端实现
```
导入 flask-wtf 实现表单的验证
from wtforms import---导入Forms
StringField---文本框
PasswordField---密码框
SubmitField---提交按钮
FileField---文件选择
TextAreaField---文本域
SelectField---下拉选择框
```
##### 登陆实现：
```
配置 csrf_token
app.config["SECRET_KEY"] = 'xxxx'
form.py 配置 与验证 拦截登陆
def admin_login_req(f): 登陆装饰器用于拦截未登陆的用户
```
##### 标签管理：
```
添加标签 标签的列表分页显示
分页操作：url_for('url',page=page)
修改:
@admin.route("/tag/edit/<int:id>", methods=['GET', 'POST'])
删除：
@admin.route("/tag/del/<int:id>/", methods=["GET"])
```
##### 电影管理：
```
添加:
MovieForm 表单中定义需要添加的组的字段
上传电影与logo文件的设置：
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
为上传文件改名：时间搓+后缀
def change_filename(filename):
    # 对文件名进行分割
    fileinfo = os.path.splitext(filename)
    # 时间搓+ uuid+ 后缀
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename
上传文件:
     # 对上传文件进行处理
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        # 上传路径是否存在
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])     # 创建文件目录
            os.chmod(app.config['UP_DIR'], 'rw')  # 读写权限
        # 改名
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        # 保存
        form.url.data.save(app.config['UP_DIR'] + url)
        form.logo.data.save(app.config['UP_DIR'] + logo)
分页显示:
    @admin.route("/movie/list/<int:page>/", methods=["GET"])
    # 从数据库关联查询
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)

删除：根据ID进行删除 def movie_del
修改：获取值进行回显：注意 文本域与下拉框不能直接赋值回显
    # 判断是什么GET请求进行回显下拉选择
    if request.method == "GET":
        form.info.data = movie.info     # 对文本域进行赋值
        form.tag_id.data = movie.tag_id # 对下拉框回显
        form.star.data = movie.star     # 对下拉框回显

```
##### 上映电影预告：
##### 用户管理：
```
用户头像目录：static/uploads/faces
模拟数据：
insert into user(name,pwd,email,phone,info,face,uuid,addtime) values('鼠','1231','1231@123.com','13888888881','鼠','1f401.png','d32a72bdac524478b7e4f6dfc8394fc0',now());
insert into user(name,pwd,email,phone,info,face,uuid,addtime) values('牛','1232','1232@123.com','13888888882','牛','1f402.png','d32a72bdac524478b7e4f6dfc8394fc1',now());
insert into user(name,pwd,email,phone,info,face,uuid,addtime) values('虎','1233','1233@123.com','13888888883','虎','1f405.png','d32a72bdac524478b7e4f6dfc8394fc2',now());
insert into user(name,pwd,email,phone,info,face,uuid,addtime) values('兔','1234','1234@123.com','13888888884','兔','1f407.png','d32a72bdac524478b7e4f6dfc8394fc3',now());
insert into user(name,pwd,email,phone,info,face,uuid,addtime) values('龙','1235','1235@123.com','13888888885','龙','1f409.png','d32a72bdac524478b7e4f6dfc8394fc4',now());
insert into user(name,pwd,email,phone,info,face,uuid,addtime) values('蛇','1236','1236@123.com','13888888886','蛇','1f40d.png','d32a72bdac524478b7e4f6dfc8394fc5',now());
insert into user(name,pwd,email,phone,info,face,uuid,addtime) values('马','1237','1237@123.com','13888888887','马','1f434.png','d32a72bdac524478b7e4f6dfc8394fc6',now());
insert into user(name,pwd,email,phone,info,face,uuid,addtime) values('羊','1238','1238@123.com','13888888888','羊','1f411.png','d32a72bdac524478b7e4f6dfc8394fc7',now());
insert into user(name,pwd,email,phone,info,face,uuid,addtime) values('猴','1239','1239@123.com','13888888889','猴','1f412.png','d32a72bdac524478b7e4f6dfc8394fc8',now());
insert into user(name,pwd,email,phone,info,face,uuid,addtime) values('鸡','1240','1240@123.com','13888888891','鸡','1f413.png','d32a72bdac524478b7e4f6dfc8394fc9',now());
insert into user(name,pwd,email,phone,info,face,uuid,addtime) values('狗','1241','1241@123.com','13888888892','狗','1f415.png','d32a72bdac524478b7e4f6dfc8394fd0',now());
insert into user(name,pwd,email,phone,info,face,uuid,addtime) values('猪','1242','1242@123.com','13888888893','猪','1f416.png','d32a72bdac524478b7e4f6dfc8394fd1',now());
用户列表展示与删除
```
##### 评论管理
```
插入测试数据
insert into comment(movie_id,user_id,content,addtime) values(7,1,"好看",now());
insert into comment(movie_id,user_id,content,addtime) values(7,2,"不错",now());
insert into comment(movie_id,user_id,content,addtime) values(7,3,"经典",now());
insert into comment(movie_id,user_id,content,addtime) values(7,4,"给力",now());
insert into comment(movie_id,user_id,content,addtime) values(8,5,"难看",now());
insert into comment(movie_id,user_id,content,addtime) values(8,6,"无聊",now());
insert into comment(movie_id,user_id,content,addtime) values(8,7,"乏味",now());
insert into comment(movie_id,user_id,content,addtime) values(8,8,"无感",now());
```
##### 电影收藏管理
```
初始化测试数据
insert into moviecol(movie_id,user_id,addtime) values(7,1,now());
insert into moviecol(movie_id,user_id,addtime) values(7,2,now());
insert into moviecol(movie_id,user_id,addtime) values(7,3,now());
insert into moviecol(movie_id,user_id,addtime) values(7,4,now());
insert into moviecol(movie_id,user_id,addtime) values(8,5,now());
insert into moviecol(movie_id,user_id,addtime) values(8,6,now());
insert into moviecol(movie_id,user_id,addtime) values(8,7,now());
insert into moviecol(movie_id,user_id,addtime) values(8,8,now());
```
##### 密码修改：
```
获取旧密码--验证旧密码--修改密码
```
##### 权限管理：
##### 角色管理：


