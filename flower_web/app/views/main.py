# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, session

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index/')
def index():
	return render_template('base.html')






	