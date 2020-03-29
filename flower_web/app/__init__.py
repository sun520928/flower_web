# -*- coding:utf-8 -*-
from flask import Flask
#from flask_session import Session
import pymysql
pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models import *
from .views.main import main
from .views.curve import curve

#创建app
def create_app():
	app = Flask(__name__)
	app.config.from_object('config.DevelopmentConfig')
	app.debug = True
	app.register_blueprint(main)
	app.register_blueprint(curve)
	db.init_app(app)
	db.create_all(app=app)
	return app