import random
import threading

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

sse_test_messages = []
@app.route('/tests/sse/', methods=['GET'])
def test_sse():
    return app.send_static_file('tests/sse.html')

import queue
class MessageAnnouncer:
    def __init__(self):
        self.listeners = []
        self.help = False
    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        q.put_nowait('data: You have successfully connected.\n\n')
        self.help = True
        return q
    def announce(self, msg):
        raise RuntimeError(self.help)
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]

announcer = MessageAnnouncer()

@app.route('/tests/sse/messagenotify/', methods=['GET'])
def message_notifier():
    def stream():
        messages = announcer.listen() # returns a queue.Queue
        while True:
            msg = messages.get() # blocks until a new message arrives
            yield msg

    return Response(stream(), content_type='text/event-stream')

@app.route('/tests/sse/sendmessage/', methods=['POST'])
def test_sse_send_message():
    global sse_test_messages
    sse_test_messages.append(request.json['data'])
    announcer.announce('data: message is here\n\n')
    return jsonify({})