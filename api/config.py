PROGRAM_NAME = 'mesothelae'

MESSAGE_DATABASE_NAME = PROGRAM_NAME + 'MessageDatabase'
MESSAGE_DATABASE_FILENAME = f'/var/www/wpd/{PROGRAM_NAME}/messages.json'

USER_DATABASE_NAME = PROGRAM_NAME + 'UserDatabase'
USER_DATABASE_FILENAME = f'/var/www/wpd/{PROGRAM_NAME}/users.json'

SESSION_ID_DATABASE_NAME = PROGRAM_NAME + 'SessionIdDatabase'
SESSION_ID_DATABASE_FILENAME = f'/var/www/wpd/{PROGRAM_NAME}/sessionIds.json'
SESSION_ID_TIMEOUT = 60 * 60 * 24 * 15 # 15 days, in seconds