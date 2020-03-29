# -*- coding: utf-8 -*-
import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

HOST = '0.0.0.0'
PORT = 5000

app = create_app()
manager = Manager(app)

if __name__ == "__main__":
    #manager.run(host=HOST, port=PORT)
    app.run(host=HOST, port=PORT, debug=True)