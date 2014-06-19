
class UserController(object):

	def get_user(self, input_var):
			# make user input lower case
			input_var_key = input_var[:1].lower()
			# a code to indicate successful resolution of user to front end script
			#code = 0
			users_dict = self.make_user_dict(self.userfile)
			# find user in dict by searching by entered username and create a list of /
			# returned values: ['username', 'guid', 'full_name']


class PhotoController(object):

	def send_picture(self, uid, image_file):

		if os.path.isfile(image_file):
			print("Sending photo...\n------------------------------------------")
			subprocess.call("curl -s -L -u tmwcolin:waitalittle -F \"photo=@/home/pi/pi-booth/app/" + \
			image_file + ";type=application/octet-stream;\" -F \"guid=" + \
			str(uid) + "\" http://gps.tmw.co.uk/ajax/photobooth.php", shell=True)
			print("\n------------------------------------------")
			
		else:
			print("Error: File not found: " + image_file)

