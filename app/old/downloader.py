import threading
from time import sleep
import urllib2

class DataDownloader(object):
	
	def __init__(self, url, cachefile, freq):
		self.url = url
		self.cachefile = cachefile
		self.freq = freq
				
	# This should run as a thread that updates the user cache file at the update frequency
	# specified.
	def update(self):
		data = urllib2.urlopen(self.url)
		file = self.cachefile

		with open(file, 'w') as f: f.write(data.read())
		print '-----> Users updated and written to ' + self.cachefile
		thr1 = threading.Timer(self.freq, self.update).start()
	
		
	def run(self):
			thr1 = threading.Timer(self.freq, self.update).start()


	'''
user_file_downloader = DataDownloader('http://www.roowilliams.com/ruh.php','cache.csv',6)
user_file_downloader.run()

while True:
	print "Spag bool"
	sleep(0.2)
	'''
