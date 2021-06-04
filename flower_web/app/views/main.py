# -*- coding:utf-8 -*-
from app.views.device import device
from flask import Blueprint, request, render_template, g

from app.models.identification import Identification

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index/')
def index():
	devices = Identification.query.all()
	content = {}
	devs = []
	for dev in devices:
		devs.append({'id': dev.id, 'description': dev.description})
	content['devices'] = devs

	g.devices = devs

	# return render_template('base.html', **content)
	return render_template('base.html')






	