# -*- coding: utf-8 -*-
from app import db

class Air(db.Model):
	index = db.Column(db.Integer, primary_key=True, autoincrement=True)
	humidity = db.Column(db.Float)
	fahrenheit = db.Column(db.Float)
	celsius = db.Column(db.Float)
	update_date = db.Column(db.DateTime, default=datetime.datetime.now)
	remarks = db.Column(db.String(256))

	def __init__(self, humidity, fahrenheit, celsius, remarks=''):
		self.humidity = humidity
		self.fahrenheit = fahrenheit
		self.celsius = celsius
		self.remarks = remarks

	def __repr__(self):
		return '<Air %f %f %f %s>' % (self.humidity, self.fahrenheit, self.celsius, self.remarks)
