# -*- coding: utf-8 -*-
from logging import debug
import os
from datetime import timedelta
# from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from logs import setup_log
from flask_login import LoginManager
from app.models.user import User

loginmanager = LoginManager()
loginmanager.session_protection = 'basic'
loginmanager.login_view = 'log_in.login'


app = create_app()
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
# manager = Manager(app)
loginmanager.init_app(app)



@loginmanager.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == "__main__":
    setup_log()
    app.run(debug=True)
