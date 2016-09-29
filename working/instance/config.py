# -*- coding:utf-8 -*-

import logging
import logging.config
import os

import yaml

# Using OS environment settings
# Generally this is where sensitive information stored ...
########################################################
for x in os.environ.keys():
    if x.startswith('APP_'):
        globals()[x.strip('APP_')] = os.environ.get(x)

# DEBUG
########################################################
VAR_DEBUG = globals().get('DEBUG')
if VAR_DEBUG is not None:
    DEBUG = VAR_DEBUG.lower() in ['true', 't', 'y', 'yes', '1']
del VAR_DEBUG

# Logging
########################################################
log_config = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'logging.yaml'
logging.config.dictConfig(yaml.load(open(log_config, 'r')))

DEBUG_LOGGER = 'debugfile'

# Mail
########################################################
if globals().get('MAIL_SERVER') is None:
    MAIL_SERVER = 'smtp.163.com'
