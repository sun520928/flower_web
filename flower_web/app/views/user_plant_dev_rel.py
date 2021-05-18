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
from app.models.relation import Relation

relations = Blueprint('relation', __name__)

@login_required
@relations.route("/relation/", methods=["GET"])
def relation():
	if request.method == 'GET':
		headers = [{
			'field': 'id',
			'title': '序号',
			'align': 'center', 
			'editable': False
		}, {
			'field': 'user_id',
			'title': '用户ID',
			'align': 'center',
			'editable': True, 
			'type': 'text',
		}, {
			'field': 'plant_id',
			'title': '植物ID',
			'align': 'center',
			'editable': True,
			'type': 'text',
		}, {
			'field': 'identification_id',
			'title': '设备ID',
			'align': 'center',
			'editable': True,
			'type': 'text',
		}]
		return render_template('list.html', url='/relation/info', headers=headers)


@login_required
@relations.route("/relation/info", methods=["POST", "GET", "DELETE"])
def relation_info():
	if request.method == 'GET':
		ret = {}
		rows = []
		rels = Relation.query.all()
		for rel in rels:
			row = {}
			row['id'] = rel.index
			row['user_id'] = rel.user_id
			row['plant_id'] = rel.plant_id
			row['identification_id'] = rel.identification_id
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
				id = int(record['id'], base=10)
				rel = Relation.query.filter_by(index=id).first()
				if rel:
					rel.user_id = record['user_id']
					rel.plant_id = record['plant_id']
					rel.identification_id = record['identification_id']
				else:
					flash('Relation:%s not existed' % id)
					flag = False
					message += 'Relation:%s not existed;' % id
			db.session.commit()

		return jsonify({'sucess': flag, 'code': 200, 'message': message})
				
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
				flash('Relation:%s not existed' % id)
				flag = False
				message += 'Relation:%s not existed;' % id
		
		return jsonify({'sucess': flag, 'code': 200, 'message': message})


	





	
