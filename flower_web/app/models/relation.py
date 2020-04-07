# -*- coding: utf-8 -*-
from app import db
import app.models.user
import app.models.identification
import app.models.plant

# class Relation(db.Model):
# 	__tablename__ = 'relation'

# 	index = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
# 	identification_id = db.Column(db.Integer, db.ForeignKey('identification.id'))

# 	def __init__(self, id, desp):
# 		self.id = id
# 		self.description = desp

# 	def __repr__(self):
# 		return '<Identification %d>' % (self.id, self.description)