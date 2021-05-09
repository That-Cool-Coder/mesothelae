import json
import os.path

from flask import Flask, jsonify, request
app = Flask(__name__)

import pythondb

from api.config import *

@app.route('/api/login', methods=['POST'])
def login():
    '''
    Expects a json request like so:
    {username : 'some string', password : 'some string'}
    '''

if __name__ == '__main__':
    app.run()