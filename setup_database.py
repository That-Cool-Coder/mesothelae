import api.pythondb as pythondb

from api.config import *

want_to_proceed = input('Warning: this will delete ALL user and message data IRREVERSIBLY. ' + 
    'Are you sure you want to proceed? Type y to proceed, type anything else to quit ') == 'y'

if not want_to_proceed:
    quit()

message_database = pythondb.createDatabase(MESSAGE_DATABASE_NAME, [],
    ['senderUsername', 'content', 'timestamp'])
pythondb.saveDatabase(message_database, MESSAGE_DATABASE_FILE_NAME)

user_database = pythondb.createDatabase(USER_DATABASE_NAME,
    ['username'], # Username must be unique
    ['displayName', 'joinTimestamp', 'passwordHash']) # These don't have to be unique
admin_user = pythondb.createRow(user_database, {
    'username' : 'ADMIN',
    'displayName' : 'ADMIN',
    'joinTimestamp' : 0,
    'passwordHash' : 'enter a password hash here'
})
pythondb.appendRow(user_database, admin_user)
pythondb.saveDatabase(user_database, USER_DATABASE_FILE_NAME)