# -*- coding: utf-8 -*-

from flask_script import Manager
from src import create_app
from gevent import monkey
monkey.patch_all()


app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""
    app.run(host='0.0.0.0', port=5000)


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
