import sys, os, time
import config

class Camera(object):
	def __init__(self):
		pass
		
	def preview(self, time, dims):
		print "Previewing image"
		os.system("raspistill -t " + str(time) + " -p " + dims)

	def take_picture(self, filename='tempimg.jpg', width=config.imgw, height=config.imgh, user='default'):
		photo = self.Photo(config.imgdir, filename, user.username, config.dims, width, height, config.countdown)
		return photo

	class Photo(object):
		def __init__(self, imgdir, filename, author, prev_dims, width, height, prev_countdown):
			self.imgdir = imgdir
			self.filename = filename
			self.full_path = imgdir + filename
			self.author = author
			self.imgw = width
			self.imgh = height
			self.preview_dimensions = prev_dims
			self.countdown = prev_countdown
			self.creation_date = time.strftime('%d-%m-%Y')
			# generate the photo using properties above
			os.system("raspistill -t " + countdown + " -o " + file_path + " -w " + \
				  imgw + " -h " + imgh + " -p " + prev_dims)
			
	def send_picture(uid, image_file):
		
		if os.path.isfile(image_file):
				print("send_picture(" + uid + "," + image_file + ")")
				os.system("curl -s -L -u tmwcolin:waitalittle -F \"photo=@/home/pi/pi-booth/app/" + \
				image_file + ";type=application/octet-stream;\" -F \"guid=" + \
				str(uid) + "\" http://gps.tmw.co.uk/ajax/photobooth.php")
		else:
			print("Error: File not found: " + image_file)
		

		#TODO: create preferences file and write to that instead of volatile var for image_count
		
		#294 = Roo's guid on the intranet.
