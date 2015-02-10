import RPi.GPIO as RPIO
import sys, os, time
import config
from models import Photo

flash_pin = 4
RPIO.setmode(RPIO.BCM) #set the way GPIO pins are counted
RPIO.setwarnings(False)
RPIO.setup(flash_pin, RPIO.OUT, initial=RPIO.HIGH)

#RPIO.output(flash_pin, True) #turn off pin

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
		
	def take_picture(self, filename='tempimg', file_extension='.jpg', width=config.imgw, height=config.imgh, user='default'):
		self.flash_on()
		time.sleep(0.5)
		photo = Photo(config.imgdir, filename, file_extension, user.username, config.dims, width, height, config.countdown, config.brightness, config.contrast, config.sharpness, config.saturation, config.awb)
		self.flash_off()
		return photo
		
	def pin_cleanup(self):
		RPIO.cleanup()
