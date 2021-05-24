# -*- coding: utf-8 -*-
from app import db

class Identification(db.Model):
	__tablename__ = 'identification'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
	description = db.Column(db.String(512))

	def __init__(self, desp):
		self.description = desp

	def __repr__(self):
		return '<Identification %d> %s' % (self.id, self.description)