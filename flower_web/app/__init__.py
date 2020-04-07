# -*- coding:utf-8 -*-
from flask import Flask
#from flask_session import Session
import pymysql
pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.air import Air
from app.models.identification import Identification
from app.models.user import User
from app.models.plant import Plant
from app.views.main import main
from app.views.curve import curve
from app.views.login import log_in

#创建app
def create_app():
	app = Flask(__name__)
	app.config.from_object('config.DevelopmentConfig')
	app.debug = True
	app.register_blueprint(main)
	app.register_blueprint(curve)
	app.register_blueprint(log_in)
	db.init_app(app)
	db.create_all(app=app)
	return app