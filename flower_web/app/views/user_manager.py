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

user_manager = Blueprint('user_manager', __name__)

@login_required
@user_manager.route("/user/", methods=["GET"])
def user():
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
			'edit': False,
		}, {
			'field': 'pwd',
			'title': '密码',
			'align': 'center',
			'edit': True,
		}]
		return render_template('list.html', url='/user/info', headers=headers)
	if request.method == 'POST':
		userid = request.form.get('userid')
		username = request.form.get('username')
		pwd = request.form.get('userpwd')
		user = User.query.filter_by(id=userid).first()
		if user:
			flash('User:%s has existed' % userid)
			return render_template('user.html')

		return render_template('list.html')        

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
		user = User.query.filter_by(id=request.json['id']).first()
		if not user:
			flash('User:%s not existed' % request.json['id'])
			return json.dumps({'sucess': False, 'code': 200, 'message': 'not existed id %s' %  request.json['id']})
		if not hasattr(user, request.json['field']):
			flash('User has not attribute %s' % request.json['field'])
			return json.dumps({'sucess': False, 'code': 200, 'message': 'User has not attribute %s' % request.json['field']})
		
		setattr(user, request.json['field'], request.json['value'])
		db.session.commit()
		return json.dumps({'sucess': True, 'code': 200})

	if request.method == 'DELETE':    
		user = User.query.filter_by(id=request.json['id'])
		if user:
			db.session.delete(user)
			db.session.commit()
			return jsonify({'sucess': True, 'code': 200})
		flash('User:%s not existed' % id)
		return jsonify({'sucess': False, 'code': 200, 'message': 'User:%s not existed' % request.json['id']})



	





	
