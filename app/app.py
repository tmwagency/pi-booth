# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from threading import Thread
import time
import urllib2
import sys
from collections import defaultdict
import config
import Queue
import camera

'''
import gaugette.rotary_encoder
import gaugette.switch

A_PIN  = 7
B_PIN  = 9
SW_PIN = 8

encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
encoder.start()
switch = gaugette.switch.Switch(SW_PIN)
last_state = None
'''

q = Queue.Queue()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}
active_guid = 0

preview_dims = '\'20,20,300,700\''

@app.route('/')
@app.route('/index')
def index():
    print ('Client at index')
    return render_template("index.html", users = return_users())

@app.route('/internal')
def internal():
    print ('Client at internal')
    return render_template("internal.html", users = return_users())

@app.route('/test')
def test():
    print ('Client at test')
    return render_template("test.html")

@socketio.on('user', namespace='/test')
def select_user(message):
	global active_guid
	user = message['data']
	print user
	guid_response = get_user_guid(user)
	response_code = guid_response[0]
	active_guid = guid_response[1]
	first_name = guid_response[2].split(" ")[0]
	emit('event', {'response': response_code, 'data': active_guid, 'name': first_name })
    
@socketio.on('my event', namespace='/test')
def test_function(message):
    print message['data']
    f = message['data']
    if f == 'takepic' and active_guid != 0:
    	camera.preview(10000,preview_dims)
        # camera.take_picture(active_guid)
    

@socketio.on('connect', namespace='/test')
def test_connect():
    print ('Client connected')
    emit('event', {'data': 'Connected'})
    '''
    for i in range(0,100):
        time.sleep(0.5)
        emit('event',{'data': 'got it!!!', 'count': i})
    time.sleep(50)
    emit('event',{'data': 'still got it!!!'})
    '''

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')



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
    socketio.run(app)
