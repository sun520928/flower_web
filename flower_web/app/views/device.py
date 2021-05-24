# -*- coding:utf-8 -*-
import logging
import datetime
import json

from flask import Blueprint, request, render_template, redirect, jsonify, flash
from flask_login import login_required
from sqlalchemy import func, desc

from app import db
from app.models.plant import Plant
from app.models.identification import Identification
from app.models.user import User

_device = Blueprint('device', __name__)


@_device.route("/device/", methods=["GET"])
@login_required
def device():
	if request.method == 'GET':
		headers = [{
			'field': 'id',
			'title': '序号',
			'align': 'center', 
			'editable': False,
		}, {
			'field': 'description',
			'title': '描述',
			'align': 'center',
			'editable': True,
			'type': 'text',
		}]

		return render_template('list.html', url='/device/info', headers=headers)


@_device.route("/device/info", methods=['GET', 'POST', 'DELETE'])
@login_required
def device_info():
	if request.method == 'GET':
		ret = {}
		rows = []
		devs = Identification.query.all()
		for dev in devs:
			row = {}
			row['id'] = dev.id
			row['description'] = dev.description
			rows.append(row)
		ret['rows'] = rows
		ret['total'] = len(rows)
		return json.dumps(ret)

	if request.method == 'POST':
		flag = True
		message = ''
		for record in request.json:
			if not record['id']:
				ident = Identification(record['description'])
				db.session.add(ident)
			else:
				ident = Identification.query.filter_by(id=record['id']).first()
				if ident:
					ident.description = record['description']
				else:
					ident = Identification(record['description'])
					db.session.add(ident)
			db.session.commit()

		return jsonify({'sucess': flag, 'code': 200, 'message': message})

	if request.method == 'DELETE':    
		ids = request.json['ids']
		flag = True
		message = ''
		for id in ids:
			ident = Identification.query.filter_by(id=id).first()
			if ident:
				db.session.delete(ident)
				db.session.commit()
			else:
				flash('Identification:%s not existed' % id)
				flag = False
				message += 'Identification:%s not existed;' % id
		
		return jsonify({'sucess': flag, 'code': 200, 'message': message})







    
