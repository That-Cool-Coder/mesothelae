import json
import os.path
import time
import uuid

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

def request_fields_valid(required_fields=[], request_json=None):
    '''
    Return a bool that states whether all of required_fields
    are in request_json
    '''
    if request_json is None:
        request_json = request.json

    return all(key in request_json for key in required_fields)

@app.route('/test-server/')
def test_server():
    return 'Successfully running app.py'

@app.route('/signin/', methods=['POST'])
def sign_in():
    '''
    Expects a json request like so:
    {username : 'some string', password : 'some string'}

    As well as the status and code, it returns this JSON:
    {sessionId : 'some string' (only included if credentials are correct)}
    '''

    # Make sure the request is valid
    if not request_fields_valid(['username', 'password']):
        return create_response(Status.WARNING, StatusCode.INVALID_REQUEST)

    try:
        # Try and find the user that matches username
        user_db = pythondb.openDatabase(USER_DATABASE_FILENAME)
        user = pythondb.getRowByUniqueField(user_db, 'username', request.json['username'])
        if user is None:
            return create_response(Status.WARNING, StatusCode.INVALID_CREDENTIALS)
        
        # Lengthy process to check if password is valid
        password_valid = False
        try:
            password_valid = hasher.verify(user['passwordHash'], request.json['password'])
        except argon2.exceptions.VerifyMismatchError:
            pass

        if not password_valid:
            return create_response(Status.WARNING, StatusCode.INVALID_CREDENTIALS)
        else:
            session_id_db = pythondb.openDatabase(SESSION_ID_DATABASE_FILENAME)

            new_session_id = str(uuid.uuid4())
            new_db_row = pythondb.createRow(session_id_db, {
                'id' : new_session_id,
                'username' : user['username'],
                'expiryTime' : time.time() + SESSION_ID_TIMEOUT
            })
            pythondb.appendRow(session_id_db, new_db_row)
            pythondb.saveDatabase(session_id_db, SESSION_ID_DATABASE_FILENAME)

            return create_response(Status.OK, StatusCode.OK,
                sessionId=new_session_id)
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

    Returns no json except for status and code
    '''

    # Make sure the request is valid
    if not request_fields_valid(['username', 'password']):
        return create_response(Status.WARNING, StatusCode.INVALID_REQUEST)
    
    if 'displayName' not in request.json:
        request.json['displayName'] = request.json['username']

    try:
        user_db = pythondb.openDatabase(USER_DATABASE_FILENAME)

        password_hash = hasher.hash(request.json['password'])
        new_user = pythondb.createRow(user_db, {
            'username' : request.json['username'],
            'displayName' : request.json['displayName'],
            'joinTimestamp' : time.time(),
            'passwordHash' : password_hash
        })
        pythondb.appendRow(user_db, new_user)
        pythondb.saveDatabase(user_db, USER_DATABASE_FILENAME)

        return create_response(Status.OK, StatusCode.OK)
        
    except pythondb.errors.FieldDuplicated:
        return create_response(Status.WARNING, StatusCode.USERNAME_NOT_UNIQUE)
    except (FileNotFoundError, PermissionError):
        return create_response(Status.ERROR, StatusCode.DATABASE_READ_ERROR)
    except pythondb.errors.FileCorrupted:
        return create_response(Status.ERROR, StatusCode.DATABASE_CORRUPTED)
    except:
        return create_response(Status.ERROR, StatusCode.UNKNOWN_ERROR)
        
@app.route('/sendmessage/', methods=['POST'])
def send_message():
    '''
    Expects a json request like so:
    {
        content : 'some string',
        sessionId : 'some string' (a valid one gotten fron /signin/)
    }

    returns no json except for status and code
    '''

    try:
        if not request_fields_valid(['content', 'sessionId']):
            return create_response(Status.WARNING, StatusCode.INVALID_REQUEST)

        session_id_db = pythondb.openDatabase(SESSION_ID_DATABASE_FILENAME)
        session_id = pythondb.getRowByUniqueField(session_id_db,
            'id', request.json['sessionId'])

        # Make sure the id exists
        if session_id is None:
            return create_response(Status.WARNING,
                StatusCode.INVALID_SESSION_ID)

        # Make sure the id is not expired
        elif session_id['expiryTime'] < time.time():
            return create_response(Status.WARNING,
                StatusCode.INVALID_SESSION_ID)
            
        # Open the message database only if the sid is valid,
        # improving strength against DDOS
        message_db = pythondb.openDatabase(MESSAGE_DATABASE_FILENAME)
        new_message = pythondb.createRow(message_db, {
            'senderUsername' : session_id['username'],
            'content' : request.json['content'],
            'timestamp' : time.time()
        })
        pythondb.appendRow(message_db, new_message)
        pythondb.saveDatabase(message_db, MESSAGE_DATABASE_FILENAME)

        return create_response(Status.OK, StatusCode.OK)

    except (FileNotFoundError, PermissionError):
        return create_response(Status.ERROR, StatusCode.DATABASE_READ_ERROR)
    except pythondb.errors.FileCorrupted:
        return create_response(Status.ERROR, StatusCode.DATABASE_CORRUPTED)
    except:
        return create_response(Status.ERROR, StatusCode.UNKNOWN_ERROR)

@app.route('/getmessages/', methods=['POST'])
def get_messages():
    '''
    Expects a json request like so:
    {
        sessionId : 'some string', (a valid one gotten fron /signin/)
        amount : 123 (optional; defaults to -1; -1 means all)
    }

    as well as status and code, returns this json:
    {
        messages = [<message object, see setup_databases.py>]
    }
    '''
    try:
        if not request_fields_valid(['sessionId']):
            return create_response(Status.WARNING, StatusCode.INVALID_REQUEST)

        session_id_db = pythondb.openDatabase(SESSION_ID_DATABASE_FILENAME)
        session_id = pythondb.getRowByUniqueField(session_id_db,
            'id', request.json['sessionId'])

        # Make sure the id exists
        if session_id is None:
            return create_response(Status.WARNING,
                StatusCode.INVALID_SESSION_ID)
                
        # Make sure the id is not expired
        elif session_id['expiryTime'] < time.time():
            return create_response(Status.WARNING,
                StatusCode.INVALID_SESSION_ID)
        
        # Only bother opening the message database if session id is valid
        message_db = pythondb.openDatabase(MESSAGE_DATABASE_FILENAME)
        amount = request.json.get('amount', 0)

        # Get messages from length - amount to end
        messages = message_db['rows'][-amount:]

        return create_response(Status.OK, StatusCode.OK, messages=messages)

    except (FileNotFoundError, PermissionError):
        return create_response(Status.ERROR, StatusCode.DATABASE_READ_ERROR)
    except pythondb.errors.FileCorrupted:
        return create_response(Status.ERROR, StatusCode.DATABASE_CORRUPTED)
    except:
        return create_response(Status.ERROR, StatusCode.UNKNOWN_ERROR)


if __name__ == '__main__':
    app.run()