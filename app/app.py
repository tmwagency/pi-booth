# -*- coding: utf-8 -*-
from flask import Flask, render_template, session
from flask.ext.socketio import SocketIO, emit
from threading import Thread
import time
import sys
from collections import defaultdict
import config
import Queue
from camera import Camera
from user import UserDataParser

q = Queue.Queue()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug=True
socketio = SocketIO(app)

# Instance of class that downloads the list of users from TMW's intranet.
# It runs continuously on a thread, updating the file at the frequency
# specified (secs): ('url','localfile',frequency)
model = UserDataParser('http://www.roowilliams.com/ruh.php','cache.csv',60)
camera = Camera()


active_guid = 0
user = None
image_file = ''
active_sessions = 0

dims = '\'282,20,460,558\''

@app.route('/')
@app.route('/index')
def index():
    print ('Client at index')
    return render_template("index.html")

@socketio.on('user', namespace='/photo')
def select_user(message):
	user_input = message['data']
	user = model.get_user(user_input)
	print user
	if not user:
		success = 0
		guid = 0
		name = user_input
	else:
		success = 1
		guid = user.guid
		name = user.first_name

	emit('event', {'response': success, 'data': guid, 'name': name})

@socketio.on('take_pic', namespace='/photo')
def take_pic(msg):

    #camera.preview(10000,config.dims)
	photo = camera.take_picture(config.imgdir,user=user)
	print photo
	emit('image', {'data': photo.full_path })

@socketio.on('send_pic', namespace='/photo')
def send_pic(message):
    global active_guid
    global image_file
    camera.send_picture(active_guid,image_file)

@socketio.on('connect', namespace='/photo')
def test_connect():
    print ('Client connected.')
    emit('event', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/photo')
def test_disconnect():
    print('Client disconnected.')
    
class MyThread(Thread):
    def __init__(self,event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(0.5):
            print "my thread"
        
if __name__ == '__main__':
    socketio.run(app,'0.0.0.0',80)
