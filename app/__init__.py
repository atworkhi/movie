# coding:utf8
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
import pymysql
import os

app = Flask(__name__)
app.debug = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:520.Xingxing@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = 'af2fad8cfe1f4c5fac4aa5edf6fcc8f3'
# Redis
app.config["REDIS_URL"] = 'redis://127.0.0.1:6379/0'
# 上传电影的路径
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
# 电影预告路径
app.config['UP_PREVIEW'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/previews/")
# 头像
app.config['UP_FACES'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/faces/")
db = SQLAlchemy(app)
rd = FlaskRedis(app)
# debug = false;
# 导入前端后端
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

# 注册蓝图
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
