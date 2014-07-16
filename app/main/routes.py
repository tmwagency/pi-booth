from flask import render_template, request
from . import main

@main.route('/')
@main.route('/index')
def index():
	print ('Web client at index')
	return render_template("index.html")

@main.route('/local')
def local_index():
	print ('Local GUI init')
	return render_template("local.html")
