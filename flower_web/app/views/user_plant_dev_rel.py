# -*- coding:utf-8 -*-
import logging
import datetime
import json

from flask import Blueprint, request, render_template, redirect, jsonify, flash, g
from flask_login import login_required, current_user
from sqlalchemy import func, desc

from app import db
from app.models.plant import Plant
from app.models.identification import Identification
from app.models.user import User
from app.models.relation import Relation

relations = Blueprint('relation', __name__)


@relations.route("/relation/", methods=["GET"])
@login_required
def relation():
	devs = []
	devices = Identification.query.all()
	for dev in devices:
		devs.append({'id': dev.id, 'description': dev.description})
	g.devices = devs

	if request.method == 'GET':
		headers = [{
			'field': 'id',
			'title': '序号',
			'align': 'center', 
			'editable': False,
			'url': ''
		}, {
			'field': 'user_id',
			'title': '用户ID',
			'align': 'center',
			'editable': True, 
			'type': 'select',
			'url': '/user/info',
		}, {
			'field': 'plant_id',
			'title': '植物ID',
			'align': 'center',
			'editable': True,
			'type': 'select',
			'url': '/plant/info',
		}, {
			'field': 'identification_id',
			'title': '设备ID',
			'align': 'center',
			'editable': True,
			'type': 'select',
			'url': '/device/info',
		}]
		return render_template('list.html', url='/relation/info', headers=headers)

@relations.route("/relation/info", methods=["POST", "GET", "DELETE"])
@login_required
def relation_info():
	devs = []
	devices = Identification.query.all()
	for dev in devices:
		devs.append({'id': dev.id, 'description': dev.description})
	g.devices = devs

	if request.method == 'GET':
		ret = {}
		rows = []
		rels = []
		if current_user.is_authenticated:
			user = User.query.filter_by(name=current_user.name).first()
			rels = Relation.query.filter_by(user_id=user.id)
		else:
			rels = Relation.query.all()
		
		for rel in rels:
			row = {}
			row['id'] = rel.index
			row['user_id'] = rel.user_id
			user = User.query.filter_by(id=rel.user_id).first()
			row['user_name'] = user.name
			row['plant_id'] = rel.plant_id
			plant = Plant.query.filter_by(id=rel.plant_id).first()
			row['plant_name'] = plant.name
			row['identification_id'] = rel.identification_id
			dev = Identification.query.filter_by(id=rel.identification_id).first()
			row['identification_desp'] = dev.description
			rows.append(row)
		ret['rows'] = rows
		ret['total'] = len(rows)
		return json.dumps(ret)

	if request.method == 'POST':
		flag = True
		message = ''
		for record in request.json:
			if not record['id']:
				rel = Relation(record['user_id'], record['plant_id'], record['identification_id'])
				db.session.add(rel)
			else:
				rel = Relation.query.filter_by(index=record['id']).first()
				if rel:
					rel.user_id = record['user_id']
					rel.plant_id = record['plant_id']
					rel.identification_id = record['identification_id']
				else:
					rel = Relation(record['user_id'], record['plant_id'], record['identification_id'])
					db.session.add(rel)
			db.session.commit()

		return jsonify({'success': flag, 'code': 200, 'message': message})
				
	if request.method == 'DELETE':    
		ids = request.json['ids']
		flag = True
		message = ''
		for id in ids:
			rel = Relation.query.filter_by(index=id).first()
			if rel:
				db.session.delete(rel)
				db.session.commit()
			else:
				flag = False
				message += 'Relation:%s not existed;' % id
		
		return jsonify({'success': flag, 'code': 200, 'message': message})


	





	
