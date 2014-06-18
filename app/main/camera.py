import RPIO
import sys, os, time
import config

import subprocess

flash_pin = 4
RPIO.setmode(RPIO.BCM) #set the way GPIO pins are counted
RPIO.setup(flash_pin, RPIO.OUT)
RPIO.output(flash_pin, True) #turn off pin

class Camera(object):
	def __init__(self):
		pass
		
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

class Photo(object):
	def __init__(self, imgdir, filename, author, preview_dims, width, height, preview_countdown):
		self.imgdir = imgdir
		self.filename = filename
		self.full_path = imgdir + filename
		self.web_path = imgdir.replace('app/','') + filename
		self.author = author
		self.imgw = width
		self.imgh = height
		self.preview_dimensions = preview_dims
		self.countdown = preview_countdown
		self.creation_date = time.strftime('%d-%m-%Y')
		# generate the photo using properties above
		os.system("raspistill -t " + preview_countdown + " -o " + imgdir + filename + " -w " + \
		width + " -h " + height + " -p " + preview_dims)
		print("raspistill -t " + preview_countdown + " -o " + imgdir + filename + " -w " + \
		width + " -h " + height + " -p " + preview_dims)
		
	def send_picture(self, uid, image_file):

		if os.path.isfile(image_file):
			print("Sending photo...\n------------------------------------------")
			subprocess.call("curl -s -L -u tmwcolin:waitalittle -F \"photo=@/home/pi/pi-booth/app/" + \
			image_file + ";type=application/octet-stream;\" -F \"guid=" + \
			str(uid) + "\" http://gps.tmw.co.uk/ajax/photobooth.php", shell=True)
			print("\n------------------------------------------")
			
		else:
			print("Error: File not found: " + image_file)
