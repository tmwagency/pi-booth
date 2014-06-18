from flask import Flask, render_template, session
from flask.ext.socketio import SocketIO, emit
from .. import socketio

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
	
@socketio.on('restart', namespace='/photo')
def restart(msg):
	end_user('end')

@socketio.on('take_pic', namespace='/photo')
def take_pic(msg):
	if len(users) > 0:
		#created a list to hold the user object globally
		user = users[0]
		filename = user.first_name + "_" + user.sir_name + ".jpg"
		photo = camera.take_picture(filename,user=user)
		photos.insert(0,photo)
		print "-----> web_path: " + photo.web_path
		emit('image', {'data': photo.web_path })
	else:
		pass
		

@socketio.on('send_pic', namespace='/photo')
def send_pic(message):
	if len(users) > 0:
		user = users[0]
		photo = photos[0]
		photo.send_picture(user.guid,photo.full_path)
		end_user('end')
		#end user session
	else:
		pass

@socketio.on('connect', namespace='/photo')
def test_connect():
    print ('Client connected.')
    emit('event', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/photo')
def test_disconnect():
    print('Client disconnected.')
