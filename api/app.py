import json
import os.path
import time

from flask import *
app = Flask(__name__)

from api import pythondb, Status, StatusCode, status
from api.config import *

import argon2
hasher = argon2.PasswordHasher()

def create_response(status, status_code, **kwargs):
    return jsonify({
        'status' : status.value,
        'statusCode' : status_code.value,
        **kwargs
    })

@app.route('/test-server/')
def test_server():
    return 'Successfully running app.py'

@app.route('/signin/', methods=['POST'])
def sign_in():
    '''
    Expects a json request like so:
    {username : 'some string', password : 'some string'}

    As well as the status and code, it returns this JSON:
    {sessionId : '' if invalid credentials, otherwise a string}
    '''

    # Make sure the request is valid
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


@app.route('/signup/', methods=['POST'])
def sign_up():
    '''
    Expects a json request like so:
    {username : 'some string',
    password : 'some string',
    displayName : 'some string' (optional, reverts to username)}
    '''

    # Make sure the request is valid
    if 'username' not in request.json or \
        'password' not in request.json:
        return create_response(Status.WARNING, StatusCode.INVALID_REQUEST)
    
    if 'displayName' not in request.json:
        request.json['displayName'] = request.json['username']

    try:
        db = pythondb.openDatabase(USER_DATABASE_FILE_NAME)

        password_hash = hasher.hash(request.json['password'])
        new_user = pythondb.createRow(db, {
            'username' : request.json['username'],
            'displayName' : request.json['displayName'],
            'joinTimestamp' : time.time(),
            'passwordHash' : password_hash
        })
        pythondb.appendRow(db, new_user)
        pythondb.saveDatabase(db, USER_DATABASE_FILE_NAME)
        
    except pythondb.errors.FieldDuplicated:
        return create_response(Status.WARNING, StatusCode.USERNAME_NOT_UNIQUE)
    except (FileNotFoundError, PermissionError):
        return create_response(Status.ERROR, StatusCode.DATABASE_READ_ERROR)
    except pythondb.errors.FileCorrupted:
        return create_response(Status.ERROR, StatusCode.DATABASE_CORRUPTED)
    except:
        return create_response(Status.ERROR, StatusCode.UNKNOWN_ERROR)

    return create_response(Status.OK, StatusCode.OK)

if __name__ == '__main__':
    app.run()