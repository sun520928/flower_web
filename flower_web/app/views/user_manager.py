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

user_manager = Blueprint('user_manager', __name__)

@login_required
@user_manager.route("/user/", methods=["GET"])
def user():
	if request.method == 'GET':
		headers = [{
			'field': 'id',
			'title': '序号',
			'align': 'center', 
			'editable': False,
		}, {
			'field': 'name',
			'title': '名称',
			'align': 'center',
			'editable': False,
		}, {
			'field': 'pwd',
			'title': '密码',
			'align': 'center',
			'editable': True,
			'type': 'text',
		}]
		return render_template('list.html', url='/user/info', headers=headers)
	if request.method == 'POST':
		flag = True
		message = ''
		for record in request.json:
			if not record['id']:
				user = User(record['name'], record['pwd'])
				db.session.add(user)
			else:
				id = int(record['id'], base=10)
				user = User.query.filter_by(id=id).first()
				if user:
					user.name = record['name']
					user.pwd = record['pwd']
				else:
					flash('User:%s not existed' % id)
					flag = False
					message += 'User:%s not existed;' % id
			db.session.commit()

		return jsonify({'sucess': flag, 'code': 200, 'message': message})

@login_required
@user_manager.route("/user/info", methods=['GET', 'POST', 'DELETE'])
def user_info():
	if request.method == 'GET':
		ret = {}
		rows = []
		users = User.query.all()
		for user in users:
			row = {}
			row['id'] = user.id
			row['name'] = user.name
			row['pwd'] = user.pwd
			rows.append(row)
		ret['rows'] = rows
		ret['total'] = len(rows)
		return json.dumps(ret)

	if request.method == 'POST':
		flag = True
		message = ''
		for record in request.json:
			if not record['id']:
				user = User(record['name'], record['pwd'])
				db.session.add(user)
			else:
				id = int(record['id'], base=10)
				user = User.query.filter_by(id=id).first()
				if user:
					user.name = record['name']
					user.pwd = record['pwd']
				else:
					flash('User:%s not existed' % id)
					flag = False
					message += 'User:%s not existed;' % id
			db.session.commit()

		return jsonify({'sucess': flag, 'code': 200, 'message': message})

	if request.method == 'DELETE':  
		ids = request.json['ids']
		flag = True
		message = ''
		for id in ids:
			user = User.query.filter_by(id=id).first()
			if user:
				db.session.delete(user)
				db.session.commit()
			else:
				flash('User:%s not existed' % id)
				flag = False
				message += 'User:%s not existed;' % id
		
		return jsonify({'sucess': flag, 'code': 200, 'message': message})  

	





	
