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

_plant = Blueprint('plant', __name__)

@login_required
@_plant.route("/plant/", methods=["POST", "GET"])
def plant():
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
			'field': 'desp',
			'title': '描述',
			'align': 'center',
		}]

		return render_template('list.html', url='/plant/info', headers=headers)
	if request.method == 'POST':
		plantname = request.form.get('plantname')
		desp = request.form.get('plantdesp')
		plant = Plant.query.filter_by(name=plantname).first()
		if plant:
			flash('Plant:%s has existed' % plantname)
			return render_template('plant.html')

		return render_template('list.html')        


@login_required
@_plant.route("/plant/info", methods=['GET'])
def plant_info():
	rows = []
	plants = Plant.query.all()
	for plant in plants:
		row = {}
		row['id'] = plant.id
		row['name'] = plant.name
		row['desp'] = plant.description
		rows.append(row)
	return json.dumps(rows)
	





    
