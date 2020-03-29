# -*- coding: utf-8 -*-
from app import db

class Identification(db.Model):
	__tablename__ = 'identification'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
	description = db.Column(db.String(512))

	def __init__(self, id, desp):
		self.id = id
		self.description = desp

	def __repr__(self):
		return '<Identification %d>' % (self.id, self.description)