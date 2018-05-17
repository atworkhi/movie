#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : forms.py
# @Author: hanxx
# @Date  : 2018/5/3
# @Desc  : 后端form表单
from flask_wtf import FlaskForm
# 字段
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
# 验证
from wtforms.validators import DataRequired, ValidationError

# 引入数据
from app.modules import Admin, Tag


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
            DataRequired('请输入您的密码!')
        ],
        description='密码',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入您的密码！",
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
    def validate_account(self, field):
        account = field.data
        # 查询账号是否存在
        admin = Admin.query.filter_by(name=account)
        if admin == 0:
            raise ValidationError('你输入的账号不存在！')


class TagForm(FlaskForm):
    '''电影标签添加'''
    # 电影标签名
    name = StringField(
        label="电影标签",
        validators=[
            DataRequired('请输入您要增加的标签！')
        ],
        description="电影标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！"
        }
    )
    submitadd = SubmitField(
        '增加标签',
        render_kw={
            "class": "btn btn-primary",
        }
    )
    submitedit = SubmitField(
        '修改标签',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class MovieForm(FlaskForm):
    '''电影相关的的表单'''
    # 电影名称
    title = StringField(
        label='电影名称',
        # 非空校验
        validators=[
            DataRequired('请输入电影名称')
        ],
        description="电影名称",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入电影名称",
        }
    )
    # 电影文件
    url = FileField(
        label='上传的电影',
        validators=[
            DataRequired("请选择电影文件")
        ],
        description='电影文件',
        render_kw={
            "id": "input_url"
        }
    )
    # 电影简介
    info = TextAreaField(
        label='电影简介',
        validators=[
            DataRequired("请输入电影简介")
        ],
        description="电影简介",
        render_kw={
            "class": "form-control",
            "rows": 10,
            "id": "input_info"
        }
    )
    # 电影封面
    logo = FileField(
        label='电影封面',
        validators=[
            DataRequired("请选择电影封面")
        ],
        description='电影封面',
        render_kw={
            "id": "input_logo"
        }
    )
    # 电影星级选择
    star = SelectField(
        label="电影星级",
        validators=[
            DataRequired("请选择电影星级")
        ],
        coerce=int,  # 转为int
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="星级",
        render_kw={
            "class": "form-control",
            "id": "input_star"
        }
    )
    # 外键管理查询所属标签
    tag_id = SelectField(
        label="电影标签",
        validators=[
            DataRequired("请选择电影标签")
        ],
        coerce=int,
        # 元组表达式查询所有标签
        choices=[(v.id, v.name) for v in Tag.query.all()],
        description="电影标签",
        render_kw={
            "class": "form-control",
            "id": "input_tag_id"
        }
    )
    # 上映地区
    area = StringField(
        label='上映地区',
        # 非空校验
        validators=[
            DataRequired('请输入电影上映地区')
        ],
        description="上映地区",
        render_kw={
            "class": "form-control",
            "id": "input_area",
            "placeholder": "请输入地区",
        }
    )
    # 片长
    length = StringField(
        label='片长',
        # 非空校验
        validators=[
            DataRequired('请输入电影片长')
        ],
        description="电影时长",
        render_kw={
            "class": "form-control",
            "id": "input_length",
            "placeholder": "请输入片长",
        }
    )
    # 上映时间
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("请选择上映时间！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请选择上映时间！",
            "id": "input_release_time"
        }
    )
    # 提交
    submitadd = SubmitField(
        '添加电影',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    # 修改
    submitedit = SubmitField(
        '修改电影',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class PreviewForm(FlaskForm):
    '''预告管理'''
    # 电影名称
    title = StringField(
        label='电影预告标题',
        # 非空校验
        validators=[
            DataRequired('请输入电影预告名称')
        ],
        description="电影预告标题",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "电影预告标题",
        }
    )

    # 电影封面
    logo = FileField(
        label='电影封面',
        validators=[
            DataRequired("请选择电影封面")
        ],
        description='电影封面',
        render_kw={
            "id": "input_logo"
        }
    )
    # 提交
    submitadd = SubmitField(
        '添加电影预告',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    # 修改
    submitedit = SubmitField(
        '修改电影预告',
        render_kw={
            "class": "btn btn-primary",
        }
    )