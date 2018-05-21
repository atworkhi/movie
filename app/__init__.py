#coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os

app = Flask(__name__)
app.debug = True
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = 'af2fad8cfe1f4c5fac4aa5edf6fcc8f3'
# 上传电影的路径
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
# 电影预告路径
app.config['UP_PREVIEW'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/previews/")
# 头像
app.config['UP_FACES'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/faces/")
db = SQLAlchemy(app)


# 导入前端后端
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

# 注册蓝图
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')