#!/usr/bin/env python
import os

from flask.ext.script import Manager, Server
from silverflask import create_app, db
from silverflask.models import User


# default to dev config because no one should use this in
# production anyway
env = os.environ.get('SILVERFLASK_ENV', 'dev')
app = create_app('silverflask.settings.%sConfig' % env.capitalize(), env=env)

manager = Manager(app)
manager.add_command("server", Server())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db, User=User)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        your Alchemy models
    """

    db.create_all()

if __name__ == "__main__":
    manager.run()
