# -*- coding: utf-8 -*-
from app import db
import app.models.user
import app.models.identification
import app.models.plant

class Relation(db.Model):
	__tablename__ = 'relation'

	index = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
	plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), index=True)
	identification_id = db.Column(db.Integer, db.ForeignKey('identification.id'))

	def __init__(self, userid, plantid, devid):
		self.user_id = userid
		self.plant_id = plantid
		self.identification_id = devid

	def __repr__(self):
		return '<Relation %d>' % (self.user_id, self.plant_id, self.identification_id)