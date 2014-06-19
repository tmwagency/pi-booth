
class UserController(object):

	def get_user(self, input_var):
			# make user input lower case
			input_var_key = input_var[:1].lower()
			# a code to indicate successful resolution of user to front end script
			#code = 0
			users_dict = self.make_user_dict(self.userfile)
			# find user in dict by searching by entered username and create a list of /
			# returned values: ['username', 'guid', 'full_name']

			model.getuser


	@threaded
	def check_user_timeout(user):
		timeout = int(config.session_timeout)
		if len(users) > 0:
			if timeout_test(timeout) is True:
				end_user('timeout')
			else:
				time.sleep(30)
				check_user_timeout(timeout)
		

	def timeout_test(timeout):
		user = users[0]
		curr_time = int(time.clock() * 1000)
		if curr_time - timeout > user.time:
			return True
		else:
			return False
		

	def end_user(reason):
	    del users[0]
	    if len(photos) > 0:
			del photos[0]
	    if reason == 'timeout':
			print "-----> User timed out"
	    elif reason == 'end':
	        pass





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


def threaded(f, daemon=False):
    import Queue

    def wrapped_f(q, *args, **kwargs):
        #this function calls the decorated function and puts the 
        #result in a queue
        ret = f(*args, **kwargs)
        q.put(ret)

    def wrap(*args, **kwargs):
        #this is the function returned from the decorator. It fires off
        #wrapped_f in a new thread and returns the thread object with
        #the result queue attached

        q = Queue.Queue()

        t = threading.Thread(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
        t.daemon = daemon
        t.start()
        t.result_queue = q        
        return t

    return wrap
   
class PhysicalInputController(object):
	



# This function creates a clean exit on ctrl+c
def signal_handler(signal, frame):
	gpio.cleanup()
	print '-----> Quit'
	sys.exit(0)
	

signal.signal(signal.SIGINT, signal_handler)