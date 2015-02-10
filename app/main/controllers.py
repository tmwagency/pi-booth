import config, models
import os, subprocess, time
from flask import session

model = models.UserDataModel(config.user_file_url,config.local_cache_file,config.cache_refresh_rate)

class UserController(object):

	def get_user(self, user_input):

		user = model.get_user(user_input)

		if not user:
			response = { 'code': 0, 'guid': 0, 'name': user_input }
			print('User ' + user_input + ' not found.')
			
		else:
			response = { 'code': 1, 'guid': user.guid, 'name': user.first_name }
			session['user'] = user
			print(session['user'])
		
		return response

			
		''' Below was my initial way to hold a user in session '''
			#users.insert(0,user)
			#check_user_timeout(user)



class PhotoController(object):

	def send_picture(self, uid, image_file):

		if os.path.isfile(image_file):
			
			print("Sending photo...")

			p = subprocess.Popen("curl -s -L -u tmwcolin:waitalittle -F \"photo=@/home/pi/pi-booth/" + \
			image_file + ";type=application/octet-stream;\" -F \"guid=" + \
			str(uid) + "\" http://gps.tmw.co.uk/ajax/photobooth.php", shell=True, stdout=subprocess.PIPE).communicate()[0]
			if 'sentok' in p:
				print 'Image sent'
				#os.remove('/home/pi/pi-booth/' + image_file)
				#os.remove('/home/pi/pi-booth/' + thumb_file)
			
		else:
			print("Error: File not found: " + image_file)

