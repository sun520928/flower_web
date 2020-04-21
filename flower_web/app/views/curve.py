# -*- coding:utf-8 -*-
import logging
import datetime
import json

from flask import Blueprint, request, render_template, redirect, jsonify
from flask_login import login_required
from sqlalchemy import func, desc

from app import db
from app.models.air import Air
from app.models.identification import Identification


curve = Blueprint('curve', __name__)

@login_required
@curve.route("/air/", methods=["POST", "GET"])
def air():
	if request.method == 'GET':
		return render_template('curve.html')
	if request.method == 'POST':
		ret = {}
		ret['code'] = 200
		ret['success'] = True
		ret['result'] = {}

		data_str = request.get_data()
		logging.debug('recv POST: %s' % data_str)
		data = json.loads(data_str.decode("utf-8"))

		humidity = float(data.get('humidity'))
		fahrenheit = float(data.get('fahrenheit'))
		celsius = float(data.get('celsius'))
		identification_id = int(data.get('id'))
		

		if humidity and fahrenheit and celsius and identification_id:
			identi = Identification.query.filter_by(
				id=identification_id).first()
			if not identi:
				ret['success'] = False
				logging.info('identification_id=%d not existed.' % identification_id)
			else:
				air = Air(humidity, fahrenheit, celsius, identification_id)
				db.session.add(air)
				db.session.commit()
				logging.info('add air success.Air=%s' % air)

		return json.dumps(ret, ensure_ascii=False)


@login_required
@curve.route("/air/info", methods=["GET"])
def info():
	ret = {}
	ret['code'] = 200
	ret['success'] = True
	ret['result'] = {}

	airs = db.session.query(
		func.max(Air.humidity).label('max_humidity'),
		func.min(Air.humidity).label('min_humidity'),
		func.max(Air.celsius).label('max_celsius'),
		func.min(Air.celsius).label('min_celsius'),
		func.date_format(Air.update_date, "%Y-%m-%d").label('date')).group_by(
			func.date_format(Air.update_date, "%Y-%m-%d").label('date')).all()
	data = dict()
	data['max_humidity'] = list()
	data['min_humidity'] = list()
	data['max_celsius'] = list()
	data['min_celsius'] = list()
	data['update_date'] = list()
	for air in airs:
		data['max_humidity'].append(air.max_humidity)
		data['min_humidity'].append(air.min_humidity)
		data['max_celsius'].append(air.max_celsius)
		data['min_celsius'].append(air.min_celsius)
		data['update_date'].append(air.date)
	ret['result'] = data

	return json.dumps(ret, ensure_ascii=False)
