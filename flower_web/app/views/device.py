# -*- coding:utf-8 -*-
import logging
import datetime
import json

from flask import Blueprint, request, render_template, redirect, jsonify
from flask_login import login_required
from sqlalchemy import func, desc

from app import db
from app.models.plant import Plant
from app.models.identification import Identification
from app.models.user import User

_device = Blueprint('device', __name__)

@login_required
@_device.route("/device/", methods=["POST", "GET"])
def device():
	if request.method == 'GET':
		headers = [{
			'field': 'id',
			'title': '序号',
			'align': 'center', 
		}, {
			'field': 'desp',
			'title': '描述',
			'align': 'center',
		}]

		return render_template('list.html', url='/device/info', headers=headers)
	if request.method == 'POST':
		devid = request.form.get('devid')
		desp = request.form.get('devdesp')
		dev = Identification.query.filter_by(id=devid).first()
		if dev:
			flash('Device:%s has existed' % devid)
			return render_template('device.html')

		return render_template('list.html')        

@login_required
@_device.route("/device/info", methods=['GET'])
def device_info():
	ret = {}
	rows = []
	devs = Identification.query.all()
	for dev in devs:
		row = {}
		row['id'] = dev.id
		row['desp'] = dev.description
		rows.append(row)
	ret['rows'] = rows
	ret['total'] = len(rows)
	return json.dumps(ret)


	





    
