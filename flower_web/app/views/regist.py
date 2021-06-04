# -*- coding:utf-8 -*-
import json
import logging

from app import db
from flask_login import login_required, login_user, logout_user
from flask import Blueprint, request, render_template, redirect, jsonify, flash, g
from app.models.user import User

registuser = Blueprint('registuser', __name__)

@registuser.route("/register/", methods=["POST", "GET"])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	else:
		username = request.form.get('username')
		usepwd = request.form.get('userpwd')
		usepwdagain = request.form.get('userpwdagain')
		user = User.query.filter_by(name=username).first()
		if user:
			flash('User:%s existed' % username)
			return render_template('register.html')
		if usepwd != usepwdagain:
			flash('Password and Confirm Password inconsistent!')
			return render_template('register.html')

		user = User(name=username, pwd=usepwd)            
		db.session.add(user)
		db.session.commit()
		return render_template('login.html')










	