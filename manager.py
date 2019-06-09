#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-31 21:24
# @Author  : ralphliu
# @Site    : 
# @File    : app.py
# @Software: PyCharm
from flask import Flask, url_for, make_response, redirect, request, session, abort, flash, render_template
import click
from urllib.parse import urlparse, urljoin
from flask_script import Manager
from jinja2.utils import generate_lorem_ipsum

app = Flask(__name__)
# 配置变量
app.config["SECRET_KEY"] = '4aa8-a690-ca241dfde751'
manager = Manager(app=app)


@app.route('/hello', defaults={'name': 'world'})
@app.route('/hello/<name>')
def index(name):
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'cookies')
    resp = render_template('base.html')
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
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
    <h1>A very long post</h1>
    <div class="body">%s</div>
    <button id="load">Load More</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $('#load').click(function(){
        $.ajax({
            url:'/more',
            type:'get',
            success:function(data){
                $('.body').append(data);}})})
    </script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)


@app.route('/flash')
def just_flash():
    flash('I am flash, who is looking for me?')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=9000, debug=True)
    manager.run()
