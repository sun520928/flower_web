# -*- coding: utf-8 -*-
from app import db

class Plant(db.Model):
	__tablename__ = 'plant'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
	name = db.Column(db.String(64))
	description = db.Column(db.String(512))

	def __init__(self, name, desp):
		self.name = name
		self.description = desp

	def __repr__(self):
		return '<Plant %d %s %s>' % (self.id, self.name, self.description)