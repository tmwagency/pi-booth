# -*- coding: utf-8 -*-
from flask import Flask, render_template, session
from flask.ext.socketio import SocketIO, emit
from threading import Thread
import time
import urllib2
import sys
from collections import defaultdict
import config
import Queue
import camera

q = Queue.Queue()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug=True
socketio = SocketIO(app)

users = {}
active_guid = 0
active_user = ''
image_file = ''
active_sessions = 0

dims = '\'282,20,460,558\''

@app.route('/')
@app.route('/index')
def index():
    print ('Client at index')
    return render_template("index.html", users = return_users())
    # return render_template("busy.html", users = return_users())

@app.route('/internal')
def internal():
    print ('Client at internal')
    return render_template("internal.html", users = return_users())

@app.route('/test')
def test():
    print ('Client at test')
    return render_template("test.html")

@socketio.on('user', namespace='/photo')
def select_user(message):
    global active_guid
    global active_user
    user = message['data']
    print user
    guid_response = get_user_guid(user)
    response_code = guid_response[0]
    active_guid = guid_response[1]
    tempname = guid_response[2].split(" ")
    first_name = tempname[0]
    sirname = tempname[1]
    active_user = first_name + "_" + sirname
    emit('event', {'response': response_code, 'data': active_guid, 'name': first_name })
    
    id = 0
    user = UserSession(id, tempname)
    user.make_active()
    id += 1
    
class UserSession(object):
    
    def __init__(self, id, username):
        self.id = id
        self.username = username
        
    def make_active(self):
        print self.username[0] + " " + self.username[1] + " is the first user."
        
@socketio.on('take_pic', namespace='/photo')
def take_pic(msg):
    if active_guid != 0:
    	#camera.preview(10000,config.dims)
        global image_file
        global active_user
        image_file = camera.take_picture(active_user,config.imgdir,config.dims,config.countdown)
        print image_file
        emit('image', {'data': image_file })

@socketio.on('send_pic', namespace='/photo')
def send_pic(message):
    global active_guid
    global image_file
    camera.send_picture(active_guid,image_file)

@socketio.on('connect', namespace='/photo')
def test_connect():
    print ('Client connected.')
    print 
    emit('event', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/photo')
def test_disconnect():
    print('Client disconnected.')
    

def init_users(q, userfile_url):
    users = defaultdict(list)
    data = urllib2.urlopen(userfile_url)

    for line in data.readlines():
        id, username, fullname = line.split(", ")
        users[username[:1].lower()].append((username, id, fullname.rstrip())) 
    q.put(users)
    print ':: Built user dict'
        
def return_users():
    global users
    thr = Thread(target=init_users, args=(q, config.user_file_url,))
    thr.start()
    thr.join()
    users = q.get()

def get_user_guid(input_var):
    input_var_key = input_var[:1].lower()
    code = 0
    try:
        guid = [s for s in users[input_var_key] if input_var in s][0][1]
        if guid:
        	full_name = [s for s in users[input_var_key] if input_var in s][0][2]
        code = 1
        guid_response = code, guid, full_name
        return guid_response
    except IndexError:
        code = 0
        guid_response = code, input_var, '0'
        
        return guid_response

        
if __name__ == '__main__':
    socketio.run(app,'0.0.0.0',80)
