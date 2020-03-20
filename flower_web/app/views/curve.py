# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect
from app import db

curve = Blueprint('curve', __name__)

@curve.route("/air/", methods=["POST", "GET"])
def air():
	ret = {}
	ret['code'] = 200
	ret['success'] = True
	ret['result'] = {}

	data_str = request.get_data()
	app.logger.debug('recv POST: %s' % data_str)
	data = json.loads(data_str.decode("utf-8"))

	if request.method =='POST':
		humidity = float(data.get('humidity'))
		fahrenheit = float(data.get('fahrenheit'))
		celsius = float(data.get('celsius'))

		if humidity and fahrenheit and celsius:
			air = Air(humidity, fahrenheit, celsius)
			db.session.add(air)
			db.session.commit()
			app.logger.info('add air success.Air=%s' % air)
	else:
		begin_date = data.get("begin")
		end_date = data.get("end")

		end_datetime = datetime.datetime.combine(end_date, datetime.time(24, 0, 0))
		begin_datetime = datetime.datetime.combine(begin_date, datetime.time(0, 0, 0))

		airs = Air.query.filter(Air.update_date < end_datetime, Air.update_date > begin_datetime).all()
		data = dict()
		data['humidity'] = list()
		data['celsius'] = list()
		for air in airs:
			data['humidity'].append(air.humidity)
			data['celsius'].append(air.celsius)
		ret['result'] = data
			
	return json.dumps(ret, ensure_ascii=False)
 

