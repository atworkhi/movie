#!/usr/bin/python
# -*- coding: utf-8 -*-
# @File  : Test.py
# @Author: hanxx
# @Date  : 2018/5/8
# @Desc  : 测试
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import os,datetime,uuid
from werkzeug.utils import secure_filename
from app.modules import Tag
# print(generate_password_hash('12345678'))
# print(check_password_hash('pbkdf2:sha256:50000$UGcv4zUD$b1e0dd104488e96bb3a49a26836d6a38c77eadfdee1d87358e75e3929d8e6e45','12345678'))
#
# file=os.path.abspath("")
# file1="中国风.mp4"
# print(secure_filename(file1))
# fileinfo = os.path.splitext(file)
# print(fileinfo)
# # 时间搓+ uuid+ 后缀
# filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
# print(filename)

for v in Tag.query.all():
    print(v.id)
    print(v.name)