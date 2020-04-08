# -*- coding:utf-8 -*-
import json
import logging

from flask_login import login_required, login_user, logout_user
from flask import Blueprint, request, render_template, redirect, jsonify
from app.models.user import User

log_in = Blueprint('log_in', __name__)

@log_in.route("/login/", methods=["POST", "GET"])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	if request.method == 'POST':
		user_info = request.json
		user = User.query.filter_by(name=user_info.get('name')).first()
		if not user:
			logging.info('User:%s not exist' % user_info.get('name'))
			return jsonify(code=200, success=False, message='User not exist.', data={})
		if user.pwd != user_info.get('pwd'):
			logging.info('Password is invalid')
			return jsonify(code=200, success=False, message='Password is invalid.', data={})

		login_user(user)
		logging.info('Logged in successfully.')
		return render_template('curve.html')

@login_required
@log_in.route("/logout/")
def logout():
	logout_user()
	logging.info('You were logged out')
	return redirect('/')








	