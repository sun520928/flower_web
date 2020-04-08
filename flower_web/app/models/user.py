# -*- coding: utf-8 -*-
from flask_login import UserMixin

from app import db

class User(db.Model, UserMixin):
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
	name = db.Column(db.String(32), unique=True, nullable=False)
	pwd = db.Column(db.String(16), nullable=False)

	def __init__(self, id, name, pwd):
		self.id = id
		self.name = name
		self.pwd = pwd

	def __repr__(self):
		return '<User %d %s>' % (self.id, self.name)