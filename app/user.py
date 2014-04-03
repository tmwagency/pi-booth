import threading
import Queue
import time, os
import urllib2
from collections import defaultdict



class UserDataParser(object):

	def __init__(self, url, cachefile, freq):
		self.url = url
		self.userfile = cachefile
		self.freq = freq
		#self.user = self.UserSession()
		downloader = self.DataDownloader(url, cachefile, freq)
		downloader.run()
	
	# create a python dictionary of users by parsing the local csv file
	# of users pulled from the intranet. This needs to happen on a thread.
	def make_user_dict(self, userfile):
		users_dict = defaultdict(list)
		data = open(userfile,'r')

		for line in data.readlines():
			id, username, fullname = line.split(", ")
			users_dict[username[:1].lower()].append((username, id, fullname.rstrip())) 
		
		print '-----> Built user dict'
		
		return users_dict
		#print users_dict

	def get_user(self, input_var):
		# make user input lower case
		input_var_key = input_var[:1].lower()
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
			
			# create a new user object
			user = self.UserSession(guid, username, full_name)
			# add the user to a list of currently active users
			print "-----> " + username

			return user

		# if a username isn't found
		except IndexError:
			return False
			
		
    
	class DataDownloader(object):

		def __init__(self, url, cachefile, freq):
			self.url = url
			self.cachefile = cachefile
			self.freq = freq
			self.update()
					
		# This should run as a thread that updates the user cache file at the update frequency
		# specified.
		def update(self):
			data = urllib2.urlopen(self.url)
			script_dir = os.path.dirname(__file__)
			rel_path = self.cachefile
			file = os.path.join(script_dir, rel_path)

			with open(file, 'a+') as f: f.write(data.read())
			print '-----> Users updated and written to ' + self.cachefile
			thr1 = threading.Timer(self.freq, self.update).start()

			
		def run(self):
				thr1 = threading.Timer(self.freq, self.update).start()
				

	class UserSession(object):

		def __init__(self, guid, username, full_name):
			self.guid = guid
			self.username = username
			self.full_name = full_name
			self.first_name = full_name.split(" ")[0]
			self.sir_name = full_name.split(" ")[1]
			self.time = int(time.clock() * 1000) # start of user session
			print "-----> " + str(self.time)
