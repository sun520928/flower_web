# -*- coding:utf-8 -*-
import logging
import datetime
import json

from flask import Blueprint, request, render_template, redirect, jsonify, g
from flask_login import login_required
from sqlalchemy import func, desc


from app import db
from app.models.air import Air
from app.models.identification import Identification


curve = Blueprint('curve', __name__)


@curve.route("/air/", methods=["POST", "GET"])
@login_required
def air():
	if request.method == 'GET':
		device_id = request.args.to_dict().get("device_id")

		devs = []
		devices = Identification.query.all()
		for dev in devices:
			devs.append({'id': dev.id, 'description': dev.description})
		g.devices = devs

		return render_template('curve.html', device_id=device_id)
		
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


@curve.route("/air/info", methods=["GET"])
@login_required
def info():
	device_id = request.args.to_dict().get("device_id")
	ret = {}
	ret['code'] = 200
	ret['success'] = True
	ret['result'] = {}

	if not device_id:
		ret['success'] = False

	airs = db.session.query(
		func.max(Air.humidity).label('max_humidity'),
		func.min(Air.humidity).label('min_humidity'),
		func.max(Air.celsius).label('max_celsius'),
		func.min(Air.celsius).label('min_celsius'),
		func.date_format(Air.update_date, "%Y-%m-%d").label('date')).group_by(
			func.date_format(Air.update_date, "%Y-%m-%d").label('date')).filter_by(identification_id=device_id).all()
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
