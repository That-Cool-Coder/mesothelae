from flask import *
from mesothelae.main import app

@app.errorhandler(400)
def error_400(e):
    return app.send_static_file('400.html'), 400

@app.errorhandler(401)
def error_401(e):
    return app.send_static_file('401.html'), 401

@app.errorhandler(403)
def error_403(e):
    return app.send_static_file('403.html'), 402

@app.errorhandler(404)
def error_404(e):
    return app.send_static_file('404.html'), 403

@app.errorhandler(418)
def error_418(e):
    return app.send_static_file('418.html'), 418