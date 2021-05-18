# -*- coding: utf-8 -*-
import os
from datetime import timedelta
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask import session
from app import create_app, db
from logs import setup_log

HOST = '0.0.0.0'
PORT = 4000

app = create_app()
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
manager = Manager(app)

if __name__ == "__main__":
    #manager.run(host=HOST, port=PORT)
    setup_log()
    app.run(host=HOST, port=PORT, debug=True)