import os
basedir = os.path.abspath(os.path.dirname(__file__))


WTF_CSRF_ENABLED = True
SECRET_KEY = "secretkey"

SQLALCHEMY_DATABASE_URI = r'sqlite:///' + os.path.join(basedir, 'site.db')
SQLALCHEMY_TRACK_MODIFICATORS = False