import os

import api.pythondb as pythondb
from api.config import *

want_to_proceed = input('Warning: this will delete ALL user and message data IRREVERSIBLY. ' + 
    'Type y to proceed, type anything else to quit ') == 'y'
if not want_to_proceed:
    quit()

message_database = pythondb.createDatabase(MESSAGE_DATABASE_NAME, [],
    ['senderUsername', 'content', 'timestamp'])
pythondb.saveDatabase(message_database, MESSAGE_DATABASE_FILENAME)
os.chmod(MESSAGE_DATABASE_FILENAME, 0o777)

user_database = pythondb.createDatabase(USER_DATABASE_NAME,
    ['username'], # Username must be unique

    ['displayName', 'joinTimestamp',
    'passwordHash']) # These don't have to be unique

admin_user = pythondb.createRow(user_database, {
    'username' : 'ADMIN',
    'displayName' : 'ADMIN',
    'joinTimestamp' : 0,
    'passwordHash' : '$argon2id$v=19$m=102400,t=2,p=8$whrMCH30ZrZYwXHLxdCKqQ$YHB8rnw3DoBHNPJdk7HdAQ'
})
pythondb.appendRow(user_database, admin_user)
pythondb.saveDatabase(user_database, USER_DATABASE_FILENAME)
os.chmod(USER_DATABASE_FILENAME, 0o777)

session_id_database = pythondb.createDatabase(SESSION_ID_DATABASE_NAME,
    ['id'], ['username', 'expiryTime'])
pythondb.saveDatabase(session_id_database, SESSION_ID_DATABASE_FILENAME)
os.chmod(SESSION_ID_DATABASE_FILENAME, 0o777)