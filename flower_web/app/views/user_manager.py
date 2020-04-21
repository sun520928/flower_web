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
@user_manager.route("/user/", methods=["POST", "GET"])
def user():
	if request.method == 'GET':
		headers = [{
			'field': 'id',
			'title': '序号',
			'align': 'center', 
		}, {
			'field': 'name',
			'title': '名称',
			'align': 'center'
		}, {
			'field': 'pwd',
			'title': '密码',
			'align': 'center',
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
@user_manager.route("/user/info", methods=['GET'])
def user_info():
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


	





	
