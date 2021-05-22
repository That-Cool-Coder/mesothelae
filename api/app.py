import json
import os.path
import time
import uuid
import atexit

from flask import *
app = Flask(__name__)

import argon2
hasher = argon2.PasswordHasher()

from api import pythondb, Status, StatusCode
from api.config import *

user_db = pythondb.openDatabase(USER_DATABASE_FILENAME)
session_id_db = pythondb.openDatabase(SESSION_ID_DATABASE_FILENAME)
message_db = pythondb.openDatabase(MESSAGE_DATABASE_FILENAME)

@atexit.register
def save_databases():
    pythondb.saveDatabase(user_db, USER_DATABASE_FILENAME)
    pythondb.saveDatabase(session_id_db, SESSION_ID_DATABASE_FILENAME)
    pythondb.saveDatabase(message_db, MESSAGE_DATABASE_FILENAME)

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
    If request_json is not specified then it defaults to flask's request.json
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
        user = pythondb.getRowByUniqueField(user_db,
            'username', request.json['username'])
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
            new_session_id = str(uuid.uuid4())
            new_db_row = pythondb.createRow(session_id_db, {
                'id' : new_session_id,
                'username' : user['username'],
                'expiryTime' : time.time() + SESSION_ID_TIMEOUT
            })
            pythondb.appendRow(session_id_db, new_db_row)

            return create_response(Status.OK, StatusCode.OK,
                sessionId=new_session_id)
    except:
        return create_response(Status.ERROR, StatusCode.UNKNOWN_ERROR)

@app.route('/signout/', methods=['POST'])
def sign_out():
    '''
    Expects a json request like so:
    {sessionId : 'some string'}

    Basically, it just finds that session id and tries to delete it

    Returns no json except for status and code
    '''

    try:
        # Make sure the request is valid
        if not request_fields_valid(['sessionId']):
            return create_response(Status.WARNING, StatusCode.INVALID_REQUEST)

        session_id = pythondb.getRowByUniqueField(session_id_db,
            'id', request.json['sessionId'])

        if session_id is None:
            return create_response(Status.WARNING, StatusCode.INVALID_SESSION_ID)
        else:
            pythondb.removeRow(session_id_db, session_id)
            return create_response(Status.OK, StatusCode.OK)

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
    
    # Fix optional parameter
    if 'displayName' not in request.json:
        request.json['displayName'] = request.json['username']

    try:
        password_hash = hasher.hash(request.json['password'])
        new_user = pythondb.createRow(user_db, {
            'username' : request.json['username'],
            'displayName' : request.json['displayName'],
            'joinTimestamp' : time.time(),
            'passwordHash' : password_hash
        })
        pythondb.appendRow(user_db, new_user)

        return create_response(Status.OK, StatusCode.OK)
        
    except pythondb.errors.FieldDuplicated:
        return create_response(Status.WARNING, StatusCode.USERNAME_NOT_UNIQUE)
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

        session_id = pythondb.getRowByUniqueField(session_id_db,
            'id', request.json['sessionId'])

        # Make sure that the id is actually valid
        if session_id is None:
            return create_response(Status.WARNING,
                StatusCode.INVALID_SESSION_ID)
        # Make sure the id is not expired
        elif session_id['expiryTime'] < time.time():
            return create_response(Status.WARNING,
                StatusCode.INVALID_SESSION_ID)
            
        new_message = pythondb.createRow(message_db, {
            'senderUsername' : session_id['username'],
            'content' : request.json['content'],
            'timestamp' : time.time()
        })
        pythondb.appendRow(message_db, new_message)

        return create_response(Status.OK, StatusCode.OK)
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
        
        # Get messages from length - amount to end
        amount = request.json.get('amount', 0)
        messages = message_db['rows'][-amount:]

        return create_response(Status.OK, StatusCode.OK, messages=messages)
    except:
        return create_response(Status.ERROR, StatusCode.UNKNOWN_ERROR)

if __name__ == '__main__':
    app.run()