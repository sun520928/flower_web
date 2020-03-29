# -*- coding: utf-8 -*-
from app import db
import datetime
import app.models.identification


class Air(db.Model):
	__tablename__ = 'air'

	index = db.Column(db.Integer, primary_key=True, autoincrement=True)
	humidity = db.Column(db.Float)
	fahrenheit = db.Column(db.Float)
	celsius = db.Column(db.Float)
	update_date = db.Column(db.DateTime, default=datetime.datetime.now)
	remarks = db.Column(db.String(256))
	identification_id = db.Column(db.Integer, db.ForeignKey('identification.id'))

	def __init__(self, humidity, fahrenheit, celsius, identification_id, remarks=''):
		self.humidity = humidity
		self.fahrenheit = fahrenheit
		self.celsius = celsius
		self.identification_id = identification_id
		self.remarks = remarks

	def __repr__(self):
		return '<Air %f %f %f %s %d>' % (self.humidity, self.fahrenheit, self.celsius, self.remarks, self.identification_id)
