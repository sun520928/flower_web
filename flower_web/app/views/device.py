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
@_device.route("/device/", methods=["GET"])
def device():
	if request.method == 'GET':
		headers = [{
			'field': 'id',
			'title': '序号',
			'align': 'center', 
			'edit': False,
		}, {
			'field': 'description',
			'title': '描述',
			'align': 'center',
			'edit': False,
		}]

		return render_template('list.html', url='/device/info', headers=headers)

@login_required
@_device.route("/device/info", methods=['GET', 'POST', 'DELETE'])
def device_info():
	if request.method == 'GET':
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

	if request.method == 'POST':
		ident = Identification.query.filter_by(id=request.json['id']).first()
		if not ident:
			flash('Identification:%s not existed' % request.json['id'])
			return json.dumps({'sucess': False, 'code': 200, 'message': 'not existed id %s' %  request.json['id']})
		if not hasattr(plant, request.json['field']):
			flash('Identification has not attribute %s' % request.json['field'])
			return json.dumps({'sucess': False, 'code': 200, 'message': 'Identification has not attribute %s' % request.json['field']})
		
		setattr(ident, request.json['field'], request.json['value'])
		db.session.commit()
		return json.dumps({'sucess': True, 'code': 200})

	if request.method == 'DELETE':    
		ident = Identification.query.filter_by(id=request.json['id'])
		if ident:
			db.session.delete(ident)
			db.session.commit()
			return jsonify({'sucess': True, 'code': 200})
		flash('Identification:%s not existed' % request.json['id'])
		return jsonify({'sucess': False, 'code': 200})


	





    
