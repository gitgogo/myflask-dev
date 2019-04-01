#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-31 21:24
# @Author  : ralphliu
# @Site    : 
# @File    : app.py
# @Software: PyCharm

from flask import Flask

app = Flask(__name__)


@app.route('/hello', defaults={'name': 'world'})
@app.route('/hello/<name>')
def index(name):
    return '<h1>Hello %s</h1>' % name


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
