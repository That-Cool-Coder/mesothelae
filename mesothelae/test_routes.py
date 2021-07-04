import random

from flask import *
from mesothelae.main import app
from mesothelae.main import socketio

@app.route('/tests/', methods=['GET'])
def test_server():
    return '<h1>Mesothelae server is responding</h1><p>(that\'s a good thing)</p>'

@app.route('/tests/param/<param>/', methods=['GET'])
def test_params(param):
    return f'You said: {param}'

@app.route('/tests/template/', methods=['GET'])
def test_templates():
    return render_template('test.html', rand_num=random.randint(0, 10))

@app.route('/tests/socket', methods=['GET'])
def test_socket():
    return app.send_static_file('socketTest.html')

@socketio.on('json')
def test_on_json():
    pass
