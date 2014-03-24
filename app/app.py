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

users_dict = {}
users = []

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

@app.route('/test')
def test():
    print ('Client at test')
    return render_template("test.html")

@socketio.on('user', namespace='/photo')
def select_user(message):
    global active_guid
    global active_user
    user_input = message['data']
    guid_response = get_user_guid(user_input)
    
    response_code = guid_response[0]
    active_guid = guid_response[1]
    tempname = guid_response[2].split(" ")
    print tempname
    first_name = tempname[0]
    sirname = tempname[1]
    active_user = first_name + "_" + sirname
    emit('event', {'response': response_code, 'data': active_guid, 'name': first_name })

class UserSession(object):

    timeout = 3000
    
    def __init__(self, guid, username, full_name):
        self.guid = guid
        self.username = username
        self.full_name = full_name
        self.first_name = full_name.split(" ")[0]
        self.sir_name = full_name.split(" ")[1]
        self.time = int(time.clock() * 1000)
        print "-----> " + str(self.time)

    def still_alive(self):
        self.time = int(time.clock() * 1000)
    
    def check_timeout(self):
        curr_time = int(time.clock() * 1000)
        print str(curr_time) + " - " + str(self.timeout) + " " + str(self.time)
        if curr_time - self.timeout > self.time:
            return True
        else:
            return False


class MyThread(Thread):
    def __init__(self,event)
        Thread.__init__(self)
        self.stopped = event

    def run(self)
        while not self.stopped.wait(0.5):
            print "my thread"



            
@socketio.on('take_pic', namespace='/photo')
def take_pic(msg):
    print users[0].check_timeout()
    users[0].still_alive()   
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
    emit('event', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/photo')
def test_disconnect():
    print('Client disconnected.')
    


 

def get_user_guid(input_var):
    #make user input lower case
    input_var_key = input_var[:1].lower()
    #a code to indicate successful resolution of user to front end script
    code = 0
    
    #find user in dict by searching by entered username and create a list of /
    #returned values: ['username', 'guid', 'full_name']
    try:
        user_list = [s for s in users_dict[input_var_key] if input_var in s][0]
        
        guid = user_list[1]
        username = user_list[0]
        print "-----> " + username
        full_name = user_list[2]
        
        #create a new user object
        user = UserSession(guid, username, full_name)
        #add the user to a list of currently active users
        users.append(user)
        print user
        print user.check_timeout()
        print user.full_name
        print user.first_name
        print user.sir_name
        #return a success code
        code = 1
        guid_response = code, user.guid, user.full_name
        return guid_response

    #if a username isn't found
    except IndexError:
        code = 0
        guid_response = code, input_var, '0' #function on the front end expects 3 vars, so sending a '0'
        return guid_response
    



def init_users(q, userfile_url):
    users_dict = defaultdict(list)
    data = urllib2.urlopen(userfile_url)

    for line in data.readlines():
        id, username, fullname = line.split(", ")
        users_dict[username[:1].lower()].append((username, id, fullname.rstrip())) 
    q.put(users_dict)
    print '-----> Built user dict'
    #print users_dict

def return_users():
    global users_dict
    thr = Thread(target=init_users, args=(q, config.user_file_url,))
    thr.start()
    thr.join()
    users_dict = q.get()
        
if __name__ == '__main__':
    socketio.run(app,'0.0.0.0',80)
