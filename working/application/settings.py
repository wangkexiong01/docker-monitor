# -*- coding: utf-8 -*-

"""
Default configurations
"""

from application.helper import gen_randomkey


# Debug
DEBUG = False

# Logger
DEBUG_LOGGER = ''

# DB
SQLALCHEMY_DATABASE_URI = 'sqlite:///../database/users.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# WTF Secret
SECRET_KEY = gen_randomkey(24)
CSRF_SESSION_KEY = gen_randomkey(24)

# Theme
THEME = 'default'

# Mail/SMS in case of destination is 139 mail
MAIL_SERVER = ''
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEBUG = False
MAIL_USERNAME = ''
MAIL_PASSWORD = ''

# Job Settings
FAILDAYS4REMOVE = 3
