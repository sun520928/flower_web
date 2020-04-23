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
			'edit': False,
		}, {
			'field': 'name',
			'title': '名称',
			'align': 'center',
			'edilt': True,
		}, {
			'field': 'description',
			'title': '描述',
			'align': 'center',
			'edit': True,
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
		id = request.json['id']
		print(id)
		plant = Plant.query.filter_by(id=request.json['id']).first()
		if not plant:
			flash('Plant:%s not existed' % request.json['id'])
			return json.dumps({'sucess': False, 'code': 200, 'message': 'not existed id %s' %  request.json['id']})
		# if not hasattr(plant, request.json['field']):
		# 	flash('Plant has not attribute %s' % request.json['field'])
		# 	return json.dumps({'sucess': False, 'code': 200, 'message': 'Plant has not attribute'})
		
		setattr(plant, request.json['field'], request.json['value'])
		print(request.json)
		print(plant)
		db.session.commit()
		return json.dumps({'sucess': True, 'code': 200})

	if request.method == 'DELETE':    
		id = request.json['id']
		plant = Plant.query.filter_by(id=id)
		if plant:
			db.session.delete(plant)
			db.session.commit()
			return jsonify({'sucess': True, 'code': 200})
		flash('Plant:%s not existed' % data['id'])
		return render_template('list.html')


	





	
