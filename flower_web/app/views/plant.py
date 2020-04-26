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

_plant = Blueprint('plant', __name__)

@login_required
@_plant.route("/plant/", methods=["GET"])
def plant():
	if request.method == 'GET':
		headers = [{
			'field': 'id',
			'title': '序号',
			'align': 'center', 
			'editable': False
		}, {
			'field': 'name',
			'title': '名称',
			'align': 'center',
			'editable': True, 
			'type': 'text',
		}, {
			'field': 'description',
			'title': '描述',
			'align': 'center',
			'editable': True,
			'type': 'text',
		}]
		return render_template('list.html', url='/plant/info', headers=headers)


@login_required
@_plant.route("/plant/info", methods=["POST", "GET", "DELETE"])
def plant_info():
	if request.method == 'GET':
		ret = {}
		rows = []
		plants = Plant.query.all()
		for plant in plants:
			row = {}
			row['id'] = plant.id
			row['name'] = plant.name
			row['description'] = plant.description
			rows.append(row)
		ret['rows'] = rows
		ret['total'] = len(rows)
		return json.dumps(ret)

	if request.method == 'POST':
		flag = True
		message = ''
		for record in request.json:
			# id = request.json['id']
			# plant = Plant.query.filter_by(id=request.json['id']).first()
			# if not plant:
			# 	flash('Plant:%s not existed' % request.json['id'])
			# 	return json.dumps({'sucess': False, 'code': 200, 'message': 'not existed id %s' %  request.json['id']})
			# if not hasattr(plant, request.json['field']):
			# 	flash('Plant has not attribute %s' % request.json['field'])
			# 	return json.dumps({'sucess': False, 'code': 200, 'message': 'Plant has not attribute %s' % request.json['field']})
			# setattr(plant, request.json['field'], request.json['value'])
			# db.session.commit()
			# return json.dumps({'sucess': True, 'code': 200})
			if not record['id']:
				plant = Plant(record['name'], record['description'])
				db.session.add(plant)
			else:
				id = int(record['id'], base=10)
				plant = Plant.query.filter_by(id=id).first()
				if plant:
					plant.name = record['name']
					plant.description = record['description']
				else:
					flash('Plant:%s not existed' % id)
					flag = False
					message += 'Plant:%s not existed;' % id
			db.session.commit()

		return jsonify({'sucess': flag, 'code': 200, 'message': message})
				
	if request.method == 'DELETE':    
		ids = request.json['ids']
		flag = True
		message = ''
		for id in ids:
			plant = Plant.query.filter_by(id=id).first()
			if plant:
				db.session.delete(plant)
				db.session.commit()
			else:
				flash('Plant:%s not existed' % id)
				flag = False
				message += 'Plant:%s not existed;' % id
		
		return jsonify({'sucess': flag, 'code': 200, 'message': message})


	





	
