# -*- coding: utf-8 -*-

import os
import json
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    PROJECT = "rinz-music-api"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = os.getenv("SECRET_KEY")


class DefaultConfig(BaseConfig):
    DEBUG = True

    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['vi']
    BABEL_DEFAULT_LOCALE = 'en'

    MONGO_URI_RINZ_MUSIC = os.getenv('MONGO_URI_RINZ_MUSIC')
    MONGO_URI_RINZ_PAYMENT = os.getenv('MONGO_URI_RINZ_PAYMENT')

    REDIS_USERS_STARTUP_NODES = json.loads(os.getenv('REDIS_USERS_STARTUP_NODES'))

    SENTRY_DSN = os.getenv('SENTRY_DSN')
