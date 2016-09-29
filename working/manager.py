# -*- coding:utf-8 -*-
import os
from string import Template

from flask.ext.script import Manager, Server, Shell, prompt_bool

from application import create_app
from application.extensions import db
from application.helper import gen_randomkey

manager = Manager(create_app('application', 'config.py'))
manager.add_command("runserver", Server('0.0.0.0', port=5000))


def _make_context():
    return dict(db=db)


manager.add_command("shell", Shell(make_context=_make_context))


@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', type=int, default=5000)
@manager.option('-w', '--workers', dest='workers', type=int, default=3)
@manager.option('-t', '--timeout', dest='timeout', type=int, default=90)
def rungunicorn(host, port, workers, timeout):
    """Start the Server with Gunicorn"""
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            return {
                'bind': '{0}:{1}'.format(host, port),
                'workers': workers, 'timeout': timeout
            }

        def load(self):
            return manager.app

    application = FlaskApplication()
    return application.run()


@manager.command
def createall():
    """Creates database tables"""
    db.create_all()


@manager.command
def dropall():
    """Drops all database tables"""
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()


@manager.option("-f", "--force", dest="force",
                help="force overwrite of existing secret_keys file", action="store_true")
@manager.option("-r", "--randomness", dest="randomness",
                help="length (randomness) of generated key; default = 24", default=24)
def gencsrfkey(force, randomness):
    """Generate random keys for CSRF and session key"""
    csrf_key = gen_randomkey(randomness)
    session_key = gen_randomkey(randomness)
    generate_keyfile(csrf_key, session_key, force)


def generate_keyfile(csrf_key, session_key, force):
    file_name = 'secret_keys.py'
    file_template = Template('''# CSRF and Session keys

CSRF_SECRET_KEY = '$csrf_key'
SESSION_KEY = '$session_key'
''')

    output = file_template.safe_substitute(dict(
        csrf_key=csrf_key, session_key=session_key
    ))

    if (os.path.exists(file_name)) and (force is False):
        print "Warning: secret_keys.py file exists.  Use '-f' flag to force overwrite."
    else:
        f = open(file_name, 'wb')
        f.write(output)
        f.close()


if __name__ == "__main__":
    manager.run()
