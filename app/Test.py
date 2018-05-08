#!/usr/bin/python
# -*- coding: utf-8 -*-
# @File  : Test.py
# @Author: hanxx
# @Date  : 2018/5/8
# @Desc  : 测试
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
print(generate_password_hash('12345678'))
print(check_password_hash('pbkdf2:sha256:50000$UGcv4zUD$b1e0dd104488e96bb3a49a26836d6a38c77eadfdee1d87358e75e3929d8e6e45','12345678'))