import threading
import Queue
import time, os
import config
import urllib2
from collections import defaultdict
from PIL import Image


''' Photo object; created when the camera captures a photo '''
class Photo(object):

	def __init__(self, imgdir, filename, file_extension, author, preview_dims, width, height, preview_countdown, brightness, contrast, sharpness, saturation, awb):

		self.imgdir = imgdir
		self.filename = filename + file_extension
		self.full_path = imgdir + filename + file_extension
		self.web_path = imgdir.replace('app/','') + filename + file_extension
		self.thumb_path = imgdir + author + config.email_domain + file_extension
		self.thumb_size = (96,96)
		self.author = author
		self.imgw = width
		self.imgh = height
		self.preview_dimensions = preview_dims
		self.countdown = preview_countdown
		self.brightness = brightness
		self.contrast = contrast
		self.sharpness = sharpness
		self.saturation = saturation
		self.awb = awb
		self.creation_date = time.strftime('%d-%m-%Y')

		# generate the photo using properties above
		os.system("raspistill -t " + preview_countdown + " -o " + self.full_path + " -w " + \
		width + " -h " + height + " -p " + preview_dims  + " -co " + contrast + " -sh " + sharpness + " -sa " + saturation + " -awb " + awb)
		print ('full_path: ' + self.full_path)

		# Process image and make thumbnail
		#self.resize_and_crop(self.full_path, self.thumb_path, self.thumb_size)
		
	def resize_and_crop(self, img_path, modified_path, size, crop_type='top'):
		"""
		Resize and crop an image to fit the specified size.

		args:
			img_path: path for the image to resize.
			modified_path: path to store the modified image.
			size: `(width, height)` tuple.
			crop_type: can be 'top', 'middle' or 'bottom', depending on this
				value, the image will cropped getting the 'top/left', 'midle' or
				'bottom/rigth' of the image to fit the size.
		raises:
			Exception: if can not open the file in img_path of there is problems
				to save the image.
			ValueError: if an invalid `crop_type` is provided.
		"""
		# If height is higher we resize vertically, if not we resize horizontally
		img = Image.open(img_path)
		# Get current and desired ratio for the images
		img_ratio = img.size[0] / float(img.size[1])
		ratio = size[0] / float(size[1])
		#The image is scaled/cropped vertically or horizontally depending on the ratio
		if ratio > img_ratio:
			img = img.resize((size[0], size[0] * img.size[1] / img.size[0]),
					Image.ANTIALIAS)
			# Crop in the top, middle or bottom
			if crop_type == 'top':
				box = (0, 0, img.size[0], size[1])
			elif crop_type == 'middle':
				box = (0, (img.size[1] - size[1]) / 2, img.size[0], (img.size[1] + size[1]) / 2)
			elif crop_type == 'bottom':
				box = (0, img.size[1] - size[1], img.size[0], img.size[1])
			else :
				raise ValueError('ERROR: invalid value for crop_type')
			img = img.crop(box)
		elif ratio < img_ratio:
			img = img.resize((size[1] * img.size[0] / img.size[1], size[1]),
					Image.ANTIALIAS)
			# Crop in the top, middle or bottom
			if crop_type == 'top':
				box = (0, 0, size[0], img.size[1])
			elif crop_type == 'middle':
				box = ((img.size[0] - size[0]) / 2, 0, (img.size[0] + size[0]) / 2, img.size[1])
			elif crop_type == 'bottom':
				box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
			else :
				raise ValueError('ERROR: invalid value for crop_type')
			img = img.crop(box)
		else :
			img = img.resize((size[0], size[1]),
					Image.ANTIALIAS)
			# If the scale is the same, we do not need to crop
		img.save(modified_path)
    
    
	def make_thumbnail(self, image, filename):
		image = Image.open(image)
		image.thumbnail((96, 96), Image.ANTIALIAS)
		image.save(filename, 'JPEG')
		print ('Thumbnail made: ' + filename)
		
		




''' This class downloads usernames and GUIDs from TMW's Intranet as a CSV '''
class UserDataModel(object):

	def __init__(self, url, cachefile, freq):
		self.url = url
		self.userfile = cachefile
		self.freq = freq
		#self.user = self.UserSession()
		downloader = self.Downloader(url, cachefile, freq)
		downloader.run()
		
		
	''' User object; created when a user logs in '''
	class User(object):

		def __init__(self, guid, username, full_name):

			self.guid = guid
			self.username = username
			self.full_name = full_name
			self.first_name = full_name.split(" ")[0]
			self.sir_name = full_name.split(" ")[1]
			self.time = int(time.clock() * 1000) # start of user session

			print "-----> " + str(self.time)
			
	
	# This gets repeated in the DataDownloader class, I couldn't figure
	# out how to reference one function from both classes.
	# Will fix when I know how.
	def userfile_path(self):
		script_dir = os.path.dirname(__file__)
		rel_path = self.userfile
		file = os.path.join(script_dir, rel_path)
		return file
		
	# create a python dictionary of users by parsing the local csv file
	# of users pulled from the intranet. This needs to happen on a thread.
	def make_user_dict(self, userfile):
		users_dict = defaultdict(list)
		data = open(self.userfile_path(),'r')
		print "-----> Data opened"

		for line in data.readlines():
			id, username, fullname, email = line.split(", ")
			users_dict[username[:1].lower()].append((username.lower(), id, fullname.rstrip())) 
		
		print '-----> Built user dict'

		
		return users_dict
		#print users_dict

	def get_user(self, input_var):
		# make user input lower case*
		input_var = input_var.lower()
		input_var_key = input_var[:1]
		
		# a code to indicate successful resolution of user to front end script
		#code = 0
		users_dict = self.make_user_dict(self.userfile)
		# find user in dict by searching by entered username and create a list of /
		# returned values: ['username', 'guid', 'full_name']
		try:
			user_list = [s for s in users_dict[input_var_key] if input_var in s][0]
			
			guid = user_list[1]
			username = user_list[0]
			full_name = user_list[2]
			
			user = self.User(guid, username, full_name)

			print "user.py -----> username: " + username
			return user

		# if a username isn't found
		except IndexError:
			return False


	class Downloader(object):

		def __init__(self, url, cachefile, freq):

			self.url = url
			self.cachefile = cachefile
			self.freq = freq
			self.update()
					
		# This should run as a thread that updates the user cache file at the update frequency
		# specified.
		def update(self):
			
			data = urllib2.urlopen(self.url)
			with open(self.userfile_path(), 'w') as f: f.write(data.read())
			print '-----> Users updated and written to ' + self.cachefile
			thr1 = threading.Timer(self.freq, self.update).start()

		def userfile_path(self):
			
			script_dir = os.path.dirname(__file__)
			rel_path = self.cachefile
			file = os.path.join(script_dir, rel_path)
			return file
		
		def run(self):
				thr1 = threading.Timer(self.freq, self.update).start()
				
		'''
		def stop(self):
				thr1_stop = threading.Event()
				thr1_stop.set()
				'''
				
