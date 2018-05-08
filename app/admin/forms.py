#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : forms.py
# @Author: hanxx
# @Date  : 2018/5/3
# @Desc  : 后端form表单
from flask_wtf import FlaskForm
# 字段
from wtforms import StringField, PasswordField, SubmitField
# 验证
from wtforms.validators import DataRequired, ValidationError
# 引入数据
from app.modules import Admin


class LoginForm(FlaskForm):
    """后台登陆表单"""
    # 账号
    account = StringField(
        label="账号",
        validators=[
            DataRequired('请输入您的账号！')
        ],
        description='用户账号',
        # 属性
        render_kw={
            "class": "form-control",
            "placeholder": "请输入您的账号！",
        }
    )
    # 密码
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码!')
        ],
        description='密码',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
        }
    )
    # 登陆按钮
    submit = SubmitField(
        '登陆',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    # 验证
    def validate_account(self,field):
        account = field.data
        # 查询账号是否存在
        admin = Admin.query.filter_by(name=account)
        if admin == 0 :
            raise ValidationError('你输入的账号不存在！')