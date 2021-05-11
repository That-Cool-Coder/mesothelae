# http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/#creating-a-wsgi-file
# http://www.enigmeta.com/2012/08/16/starting-flask/

# for Py3:
# http://askubuntu.com/questions/488529/pyvenv-3-4-error-returned-non-zero-exit-status-1

import os, sys

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, PROJECT_DIR)

from api import app as application