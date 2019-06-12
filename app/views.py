#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-12 07:39
# @Author  : ralphliu
# @Site    : 
# @File    : views.py
# @Software: PyCharm

from flask import render_template, Blueprint

blue = Blueprint('first_blue', __name__)

# 使用blue不生效, 改用app
# @blue.errorhandler(404)
# def page404(e):
#     return render_template('errors/404.html'), 404


@blue.route('/hello404')
def hello404():
    return render_template('errors/404.html')
