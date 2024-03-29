# -*- coding:utf-8 -*-
import json
import logging

from flask_login import login_required, login_user, logout_user
from flask import Blueprint, request, render_template, redirect, jsonify, flash, g
from app.models.user import User
from app.models.identification import Identification

log_in = Blueprint('log_in', __name__)

@log_in.route("/login/", methods=["POST", "GET"])
def login():
	devs = []
	devices = Identification.query.all()
	for dev in devices:
		devs.append({'id': dev.id, 'description': dev.description})
	g.devices = devs
	
	if request.method == 'GET':
		return render_template('login.html')
	else:
		username = request.form.get('username')
		usepwd = request.form.get('userpwd')
		user = User.query.filter_by(name=username).first()
		if not user:
			flash('User:%s not exist' % username)
			return render_template('login.html')
		if user.pwd != usepwd:
			flash('Password is invalid')
			return render_template('login.html')

		login_user(user)
		return redirect('/relation')

		

@login_required
@log_in.route("/logout/")
def logout():
	logout_user()
	flash('You were logged out.')
	return redirect('/')








	