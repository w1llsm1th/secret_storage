#!/usr/bin/env python

import json

from flask import Flask, request, session, redirect, url_for, render_template

app = Flask(__name__)

github_addr = 'https://github.com/w1llsm1th/secret_storage'

with open('config.json', 'r') as json_data:
    config = json.load(json_data)


users = [
    {'user_id': 1, 'username': 'admin', 'password': 'admin'},
    {'user_id': 2, 'username': 'test', 'password': 'test'},
    {'user_id': 3, 'username': 'cisco', 'password': 'cisco'},
]

# TODO: auth
def handle_request(request):
    args = request.form

    if not args.has_key('username') or not args.has_key('password'):
        pass

    return render_template('index.html')

def get_answer(level):
    if isinstance(level, int):
        level = str(level)

    return {
        '0': '1995',
        '1': '91',
        '2': '127081',
    }.get(level, 'nope')

def get_quiz(level):
    if isinstance(level, int):
        level = str(level)

    return {
        '0': 'The year I was born ____',
        '1': 'My school number in Moscow __ (the one in Arbat district)',
        '2': 'My Moscow mailing index ______',
        '3': github_addr,
    }.get(level, 'nope')


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return handle_request(request)

    if session.get('user_id', 0) == 1:
        return render_template('admin_dashboard.html') # <-- Yep, flag stored in here
    return render_template('index.html')

@app.route('/recover')
def restore_password():
    level = session.get('level', None)
    if level is None:
        level = 0
        session['level'] = 0

    quiz = get_quiz(level)
    return render_template('level.html', quiz=quiz)

@app.route('/answer', methods=['POST'])
def answer():
    args = request.form
    level = session.get('level', None)

    if level is None:
        return render_template('index.html')

    if not args.has_key('answer'):
        return render_template('index.html')
    print get_answer(level)
    print args['answer']
    if get_answer(level) == args['answer']:
        session['level'] += 1
        return render_template('index.html', success='correct!')
    return render_template('index.html', err='wrong answer')

if __name__ == '__main__':
    app.config = dict(app.config, **config)
    app.secret_key = config['secret_key']
    app.threaded = True
    app.processes = 50
    app.run(host=config['host'], port=config['port'])

