# -*- coding: utf-8 -*-
from flask import Flask, render_template, session
from flask.ext.socketio import SocketIO, emit
import threading
import time
import sys
from collections import defaultdict
import config
import Queue
from camera import Camera
from user import UserDataParser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug=True
socketio = SocketIO(app)

# Instance of class that downloads the list of users from TMW's intranet.
# It runs continuously on a thread, updating the file at the frequency
# specified (secs): ('url','localfile',frequency)
model = UserDataParser('http://www.roowilliams.com/ruh.php','cache.csv',60)
camera = Camera()

users = []
photos = []
queue = Queue.Queue()


dims = '\'282,20,460,558\''

@app.route('/')
@app.route('/index')
def index():
    if len(users) > 0: # if we already have an active user
        print ('New client at index, app busy')
        return render_template("busy.html")
    else:
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
		users.insert(0,user)
		check_user_timeout(user)

	emit('event', {'response': success, 'data': guid, 'name': name})

@socketio.on('take_pic', namespace='/photo')
def take_pic(msg):
    #created a list to hold the user object globally
    user = users[0]
    filename = user.first_name + "_" + user.sir_name + ".jpg"
    photo = camera.take_picture(filename,user=user)
    photos.insert(0,photo)
    print "-----> web_path: " + photo.web_path
    emit('image', {'data': photo.web_path })

@socketio.on('send_pic', namespace='/photo')
def send_pic(message):
    user = users[0]
    photo = photos[0]
    camera.send_picture(user.guid,photo.full_path)
    end_user('end')
    #end user session

@socketio.on('connect', namespace='/photo')
def test_connect():
    print ('Client connected.')
    emit('event', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/photo')
def test_disconnect():
    print('Client disconnected.')


def end_user(reason):
    del users[0]
    del photos[0]
    if reason == 'timeout':
        emit('event', {'data': 'timeout'})
    elif reason == 'end':
        pass

def check_user_timeout(user):
    thread = threading.Timer(1, user.check_timeout, queue).start()
    print ":: " + str(queue.qsize())


'''
class MyThread(Thread):
    def __init__(self,event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(0.5):
            print "my thread"
'''
if __name__ == '__main__':
    socketio.run(app,'0.0.0.0',80)
