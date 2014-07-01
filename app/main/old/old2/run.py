# -*- coding: utf-8 -*-

from flask import Flask, render_template, session
from flask.ext.socketio import SocketIO, emit
import threading, Queue
import time, sys, os, signal
from collections import defaultdict
import RPIO as gpio

import camera
import model

import config




	
#import RPIO as gpio
#gpio.setmode(gpio.BCM)




# Instance of class that downloads the list of users from TMW's intranet.
# It runs continuously on a thread, updating the file at the frequency
# specified (secs): ('url','localfile',frequency)

window = Window()



dims = '\'282,20,460,558\''

reset_pin = 27






def restart_program(gpio_id, value):
	print "-----> Restart"
	try:
		gpio.cleanup()
		python = sys.executable
		os.execl(python, python, * sys.argv)
	except Exception as e:
		print e

'''		
gpio.wait_for_interrupts(threaded=True)

gpio.add_interrupt_callback(
reset_pin, \
restart_program, \
edge='both', \
pull_up_down=gpio.PUD_UP, \
threaded_callback=False, \
debounce_timeout_ms=20)
'''






if __name__ == '__main__':
    socketio.run(app,'0.0.0.0',80)
