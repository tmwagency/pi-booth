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
    user = message['data']
    print user
    guid_response = get_user_guid(user)
    emit('event', {'data': guid_response })
    
@socketio.on('my event', namespace='/test')
def test_function(message):
    print message['data']
    f = message['data']
    if f == 'takepic':
        camera.take_picture(294)
    

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
        id, username, _ = line.split(", ", 2)
        users[username[:1].lower()].append((username, id))     
    q.put(users)
    print '---------------got users'
        
def return_users():
    global users
    thr = Thread(target=init_users, args=(q, config.user_file_url,))
    thr.start()
    thr.join()
    users = q.get()

def get_user_guid(input_var):
    input_var_key = input_var[:1].lower()
    try:
        guid = [s for s in users[input_var_key] if input_var in s][0][1]
        return guid
        print ("The guid for your username is: " + guid)
    except IndexError:
        print "Username not found, try again or type 'c' to cancel."
        return "err: " + input_var

def user_not_found(input):
    emit('event', {'data': '404 ' + input})


'''
idle = 0
idle_counter = 0
idle = True

while True:
    time.sleep(0.01)
    delta = encoder.get_delta()

    if delta != 0:
        print delta
        idle_counter = 100
        idle = False

    elif not idle:
        print "not idle"
        if idle_counter > 0:
            idle_counter -= 1
        else:
            print "idle"
            idle = True
'''

if __name__ == '__main__':
    socketio.run(app)
