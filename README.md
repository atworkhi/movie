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
 manage.py 入口启动脚本
 app 项目目录
 __init__.py  初始化文件
 models.py    数据模型文件
 static         静态资源文件
 home/admin     前后台模块
 views.py       视图处理文件
 forms.py       表单处理文件
 templates      模版目录
```




