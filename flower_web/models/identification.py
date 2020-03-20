# -*- coding: utf-8 -*-

class Identification(db.Model):
	index = db.Column(db.Integer, primary_key=True, autoincrement=True)
	id = db.Column(db.Integer)
	description = db.Column(db.String(512))

	def __init__(self, id, desp):
		self.id = id
		self.description = desp

	def __repr__(self):
		return '<Identification %d>' % self.id