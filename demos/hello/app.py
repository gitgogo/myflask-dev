#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-31 21:24
# @Author  : ralphliu
# @Site    : 
# @File    : app.py
# @Software: PyCharm
from flask import Flask, url_for, make_response, redirect, request, session, abort
import click

app = Flask(__name__)
# 配置变量
app.config["SECRET_KEY"] = '4aa8-a690-ca241dfde751'


@app.route('/hello', defaults={'name': 'world'})
@app.route('/hello/<name>')
def index(name):
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'cookies')
    resp = '<h1>Hello %s</h1>' % url_for('index', name=name, _external=True)
    if 'logged_in' in session:
        resp += '[Authenticated]'
    else:
        resp += '[No Authenticated]'
    return resp


@app.cli.command()
def hello():
    click.echo('hello, human')


@app.route('/302/<name>', methods=['GET', 'POST'])
def reback(name):
    resp = make_response(redirect(url_for('index', name=name)))
    resp.set_cookie('name', name)
    return resp


@app.route('/hello2/')
def hello2():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'cookie')
    return '<h1>hello2, %s</h1>' % name


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('index'))


@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'welcome to admin page'


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('index'))


@app.route('/foo')
def foo():
    return '<h1>Foo Page<h1><a href="%s">do something and redirect</a>' % url_for('do_something', next=request.full_path)


@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">do something and redirect</a>' % url_for('do_something', next=request.full_path)


@app.route('/do_something')
def do_something():
    return redirect_back()


def redirect_back(default='index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if target:
            return redirect(target)
    return redirect(url_for(default, **kwargs))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
