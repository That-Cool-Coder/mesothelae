from flask import *
from mesothelae.main import app


# A dict of errorcode : information to use for HTTP error pages
ERROR_PAGE_DATA = {
    400 : 'Bad request.',
    401 : 'Access is denied to this page.',
    403 : 'You are forbidden to view this page.',
    404 : 'The page you are looking for does not exist.',
    418 : 'I\'m a teapot!'
}

class ErrorPageInterface:
    '''This is a simple class designed to allow creating error pages
    from a dict instead of hard-coding each one in its own function.
    It acts exactly like a hard-coded function but is configured
    '''

    def __init__(self, code, message):
        self.code = code
        self.message = message
    
    def __call__(self, *args, **kwds):
        return render_template('httpError.html', code=self.code, message=self.message)

for error_code in ERROR_PAGE_DATA:
    interface = ErrorPageInterface(error_code, ERROR_PAGE_DATA[error_code])
    app.errorhandler(error_code)(interface)