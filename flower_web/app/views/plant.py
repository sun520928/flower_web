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
			if not record['id']:
				plant = Plant(record['name'], record['description'])
				db.session.add(plant)
			else:
				plant = Plant.query.filter_by(id=record['id']).first()
				if plant:
					plant.name = record['name']
					plant.description = record['description']
				else:
					plant = Plant(record['name'], record['description'])
					db.session.add(plant)

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


	





	
