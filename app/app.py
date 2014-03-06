from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from threading import Thread
import user
import time



        


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", users = user.return_users())

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

if __name__ == '__main__':
    socketio.run(app)

