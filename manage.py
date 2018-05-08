#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : manage.py
# @Author: hanxx
# @Date  : 2018/5/3
# @Desc  : 程序入口

from app import app
from app.modules import *
from app import db


if __name__ == "__main__":
    app.run()