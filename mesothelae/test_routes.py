import random
import time
import itertools

import asyncio
from flask import *
from mesothelae.main import app

@app.route('/tests/', methods=['GET'])
def test_server():
    return '<h1>Mesothelae server is responding</h1><p>(that\'s a good thing)</p>'

@app.route('/tests/param/<param>/', methods=['GET'])
def test_params(param):
    return f'You said: {param}'

@app.route('/tests/template/', methods=['GET'])
def test_templates():
    return render_template('tests/test.html', rand_num=random.randint(0, 10))

@app.route('/tests/sse/', methods=['GET'])
def test_sse():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            for i, c in enumerate(itertools.cycle('\|/-')):
                yield "data: %s %d\n\n" % (c, i)
                time.sleep(.1)  # an artificial delay
        return Response(events(), content_type='text/event-stream')
    return redirect(url_for('static', filename='/tests/sse.html'))