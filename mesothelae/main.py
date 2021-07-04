from flask import *
from flask_socketio import SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

from mesothelae import test_routes, error_page_routes

if __name__ == '__main__':
    socketio.run(app)