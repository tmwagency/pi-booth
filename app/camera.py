import sys, os, time




def take_picture(uid):
        image_count = 1
        countdown_time = 3000
	strImage = "image" + str(image_count) + ".jpg"
        os.system("raspistill -t " + str(countdown_time) + " -o " + strImage)
        image_count = image_count + 1
	print("Image name:" + strImage)
	send_picture(uid,strImage)
	print("uid:" + str(uid))

def send_picture(uid,filename):
	os.system("curl -s -L -u tmwcolin:waitalittle -F \"photo=@/home/pi/" + filename + ";type=application/octet-stream;\" -F \"guid=" + str(uid) + "\" http://gps.tmw.co.uk/ajax/photobooth.php")
	print("Image sent.")
	

	#TODO: create preferences file and write to that instead of volatile var
	
	#294 = Roo's guid on the intranet.
	

        #the following is used to email a picture
	#os.system("mpack -s \"Your Photo\" " + strImage + " roowilliams@gmail.com")
