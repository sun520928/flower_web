# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect
from app import db
from sqlalchemy import func, desc
import json
from app.models.air import Air


curve = Blueprint('curve', __name__)

@curve.route("/air/", methods=["POST", "GET"])
def air():
	ret = {}
	ret['code'] = 200
	ret['success'] = True
	ret['result'] = {}

	data_str = request.get_data()
	#app.logger.debug('recv POST: %s' % data_str)
	print('recv POST: %s' % data_str)
	data = json.loads(data_str.decode("utf-8"))

	if request.method =='POST':
		humidity = float(data.get('humidity'))
		fahrenheit = float(data.get('fahrenheit'))
		celsius = float(data.get('celsius'))
		identification_id = int(data.get('id'))

		if humidity and fahrenheit and celsius and identification_id:
			air = Air(humidity, fahrenheit, celsius, identification_id)
			db.session.add(air)
			db.session.commit()
			#app.logger.info('add air success.Air=%s' % air)
			print('add air success.Air=%s' % air)
	else:
		begin_date = data.get("begin")
		end_date = data.get("end")

		end_datetime = datetime.datetime.combine(end_date, datetime.time(24, 0, 0))
		begin_datetime = datetime.datetime.combine(begin_date, datetime.time(0, 0, 0))

		#airs = Air.query.filter(Air.update_date < end_datetime, Air.update_date > begin_datetime).all()
		airs = db.session.query(func.date_formate(Air.update_date, '%Y-%m-%d').label('date'),
		func.max(Air.humidity),
		func.min(Air.humidity),
		func.max(Air.celsius),
		func.min(Air.celsius))
		data = dict()
		data['max_humidity'] = list()
		data['min_humidity'] = list()
		data['max_celsius'] = list()
		data['min_celsius'] = list()
		data['update_date'] = list()
		for air in airs:
			data['humidity'].append(air.humidity)
			data['celsius'].append(air.celsius)
			data['update_date'].append(air.update_date)
		ret['result'] = data
			
	return json.dumps(ret, ensure_ascii=False)
 

