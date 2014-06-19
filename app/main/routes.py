from flask import render_template, request
from . import main

@main.route('/')
@main.route('/index')
def index():
	
	print ('Client at index')
	return render_template("index.html")
