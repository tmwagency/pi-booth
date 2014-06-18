from flask import render_template, request
from . import main

@main.route('/')
@main.route('/index')
def index():
    if len(users) > 0: # if we already have an active user
        print ('New client at index, app busy')
        return render_template("busy.html")
    else:
        print ('Client at index')
        return render_template("index.html")
