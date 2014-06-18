#!/usr/bin/python
from app import create_app, socketio

app = create_app(True)

if __name__ == '__main__':
	socketio.run(app)
