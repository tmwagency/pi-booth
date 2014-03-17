import sys, os, time
import config

def preview(time,dims):
        print "Previewing image"
	os.system("raspistill -t " + str(time) + " -p " + dims)

def take_picture(uid,dims):
        image_count = 1
        countdown_time = 3000
	strImage = "image" + str(image_count) + ".jpg"
        os.system("raspistill -t " + str(countdown_time) + " -o " + strImage + " -p " + dims)
        image_count = image_count + 1
	print("Image name:" + strImage)
	send_picture(uid,strImage)
	print("uid:" + str(uid))

def send_picture(uid,filename):
	print("send_picture(" + uid + "," + filename + ")")
	if os.path.isfile(filename):
		os.system("curl -s -L -u tmwcolin:waitalittle -F \"photo=@/home/pi/" + filename + ";type=application/octet-stream;\" -F \"guid=" + str(uid) + "\" http://gps.tmw.co.uk/ajax/photobooth.php")
	else:
		print("Error: File not found.")
	

	#TODO: create preferences file and write to that instead of volatile var for image_count
	
	#294 = Roo's guid on the intranet.
