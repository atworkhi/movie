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


