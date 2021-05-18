# -*- coding:utf-8 -*-
import os
from flask import Flask
from flask_login import LoginManager
#from flask_session import Session
import pymysql
pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

from app.models.air import Air
from app.models.identification import Identification
from app.models.user import User
from app.models.plant import Plant
from app.models.relation import Relation

from app.views.main import main
from app.views.curve import curve
from app.views.login import log_in
from app.views.regist import registuser
from app.views.plant import _plant
from app.views.device import _device
from app.views.user_manager import user_manager
from app.views.user_plant_dev_rel import relations

#创建app
def create_app():
	app = Flask(__name__)
	app.config.from_object('config.DevelopmentConfig')
	app.debug = True

	app.register_blueprint(main)
	app.register_blueprint(curve)
	app.register_blueprint(log_in)
	app.register_blueprint(registuser)
	app.register_blueprint(_plant)
	app.register_blueprint(_device)
	app.register_blueprint(user_manager)
	app.register_blueprint(relations)

	db.init_app(app)
	db.create_all(app=app)

	login_manager.login_view = "login"
	login_manager.init_app(app)
	return app

@login_manager.user_loader
def load_user(userid):
	return User.query.get(int(userid))