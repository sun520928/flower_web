# -*- coding:utf-8 -*-
import json
import logging

from flask import Blueprint, request, render_template, redirect
from app.models.user import User

log_in = Blueprint('login', __name__)

@log_in.route("/login/", methods=["POST", "GET"])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	if request.method == 'POST':
		ret = {}
		ret['code'] = 200
		ret['success'] = True

		user_info = request.form.to_dict()
		user = User.query.filter_by(name=user_info.get('name')).first()
		if not user:
			ret['success'] = False
			ret['result'] = 'User not exist.'
		elif user.pwd != user_info.get('pwd'):
			ret['success'] = False
			ret['result'] = 'Password is invalid.'

		return json.dumps(ret, ensure_ascii=False)







	