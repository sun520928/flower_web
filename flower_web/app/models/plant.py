# -*- coding: utf-8 -*-
from app import db

class Plant(db.Model):
	__tablename__ = 'plant'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
	description = db.Column(db.String(512))

	def __init__(self, id, desp):
		self.id = id
		self.description = desp

	def __repr__(self):
		return '<Plant %d>' % (self.id, self.description)