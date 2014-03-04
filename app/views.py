from flask import render_template
from app import app, user

@app.route('/')
@app.route('/index')
def index():
    
    return render_template("index.html", users = user.return_users())
