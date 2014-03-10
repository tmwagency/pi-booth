from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from threading import Thread
import user
import time
import urllib2
import sys
from collections import defaultdict
import config
import Queue
import gaugette.rotary_encoder
import gaugette.switch

A_PIN  = 7
B_PIN  = 9
SW_PIN = 8

encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
switch = gaugette.switch.Switch(SW_PIN)
last_state = None

q = Queue.Queue()


        


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", users = return_users())

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('event', {'data': 'Connected'})
    for i in range(0,100):
        time.sleep(0.5)
        emit('event',{'data': 'got it!!!', 'count': i})
    time.sleep(50)
    emit('event',{'data': 'still got it!!!'})

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
    thr = Thread(target=init_users, args=(q, config.user_file_url,))
    thr.start()
    thr.join()
    users = q.get()
    # users = init_users(config.user_file_url)
    return users

print encoder.get_delta()

if __name__ == '__main__':
    socketio.run(app)
