import RPIO
import sys, os, time
import config
import subprocess
import controller

flash_pin = 4
RPIO.setmode(RPIO.BCM) #set the way GPIO pins are counted
RPIO.setup(flash_pin, RPIO.OUT)
RPIO.output(flash_pin, True) #turn off pin

class CameraController(object):
	
	def preview(self, time, dims):
		print "Previewing image"
		os.system("raspistill -t " + str(time) + " -p " + dims)
		
	def flash_on(self):
		RPIO.output(flash_pin, False)
		print "Flash: ON"
		
	def flash_off(self):
		RPIO.output(flash_pin, True)
		print "Flash: OFF"
		
	def take_picture(self, filename='tempimg.jpg', width=config.imgw, height=config.imgh, user='default'):
		self.flash_on()
		time.sleep(0.5)
		photo = Photo(config.imgdir, filename, user.username, config.dims, width, height, config.countdown)
		self.flash_off()
		return photo
