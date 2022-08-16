# -*- coding: utf-8 -*-


# File: manage.py
"""
   Description:
        -
        -
"""
from gevent import monkey

monkey.patch_all()

from src import create_app
from flask_script import Manager
import asyncio
import threading

app = create_app()
manager = Manager(app)

@manager.command
def run():
    """Run in local machine."""
    # TODO set debug to False
    app.run(host='0.0.0.0', port="5004", debug=False)

manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()