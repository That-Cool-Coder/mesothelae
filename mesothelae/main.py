from flask import *
app = Flask(__name__)

from mesothelae import test_routes, error_page_routes

if __name__ == '__main__':
    app.run()