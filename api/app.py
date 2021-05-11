import json
import os.path

from flask import *
app = Flask(__name__)

from api import pythondb, Status, StatusCode
from api.config import *

import argon2
hasher = argon2.PasswordHasher()

def create_response(status, status_code, **kwargs):
    return jsonify({
        'status' : status,
        'statusCode' : status_code,
        **kwargs
    })

@app.route('/testserver/')
def test_server():
    return 'Successfully running app.py'

@app.route('/api/login', methods=['POST'])
def login():
    '''
    Expects a json request like so:
    {username : 'some string', password : 'some string',
        displayName : 'some string' (optional, reverts to username)}

    As well as the status and code, it returns this JSON:
    {sessionId : '' if invalid credentials, otherwise a string}
    '''

    # Make sure the request if valid
    if 'username' not in request.json or \
        'password' not in request.json:
        return create_response(Status.WARNING, StatusCode.INVALID_REQUEST)

    try:
        # Try and find the user that matches username
        db = pythondb.openDatabase(USER_DATABASE_FILE_NAME)
        user = pythondb.getRowByUniqueField(db, 'username', request.json['username'])
        if user is None:
            return create_response(Status.WARNING, StatusCode.INVALID_CREDENTIALS)
        
        # Lengthy process to check if password is valid
        password_valid = False
        try:
            password_valid = hasher.verify(user['passwordHash'], request.json['password'])
        except argon2.exceptions.VerifyMismatchError:
            pass

        # This should be the main 
        if password_valid:
            return create_response(Status.WARNING, StatusCode.OK)
        else:
            return create_response(Status.WARNING, StatusCode.INVALID_CREDENTIALS)
    except (FileNotFoundError, PermissionError):
        return create_response(Status.ERROR, StatusCode.DATABASE_READ_ERROR)
    except pythondb.errors.FileCorrupted:
        return create_response(Status.ERROR, StatusCode.DATABASE_CORRUPTED)
    except:
        return create_response(Status.ERROR, StatusCode.UNKNOWN_ERROR)


@app.route('/api/createuser', methods=['POST'])
def create_user():
    '''
    Expects a json request like so:
    {username : 'some string', password : 'some string'}
    '''

if __name__ == '__main__':
    app.run()