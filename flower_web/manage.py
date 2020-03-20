# -*- coding: utf-8 -*-
import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

app = create_app()
manager = Manager(app)

if __name__ == "__main__":
    manager.run()
