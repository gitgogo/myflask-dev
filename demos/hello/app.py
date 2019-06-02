#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-31 21:24
# @Author  : ralphliu
# @Site    : 
# @File    : app.py
# @Software: PyCharm
from flask import Flask, url_for, make_response, redirect
import click

app = Flask(__name__)
# 配置变量
app.config["SECRET_KEY"] = '4aa8-a690-ca241dfde751'


@app.route('/hello', defaults={'name': 'world'})
@app.route('/hello/<name>')
def index(name):
    return '<h1>Hello %s</h1>' % url_for('index', name=name, _external=True)


@app.cli.command()
def hello():
    click.echo('hello, human')


@app.route('/302/<name>', methods=['GET', 'POST'])
def reback(name):
    resp = make_response(redirect(url_for('index', name=name)))
    resp.set_cookie('name', name)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
