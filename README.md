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
#### 数据库  flask-sqlalchemy
安装：
> pip install flask-sqlalchemy

链接：
```text

```





