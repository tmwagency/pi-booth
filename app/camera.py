import sys, os, time
import config

def preview(time,dims):
    print "Previewing image"
    os.system("raspistill -t " + str(time) + " -p " + dims)

def take_picture(name,imgdir,dims,countdown):
    image = imgdir + name + "-" + time.strftime('%d-%m-%Y') + ".jpg"
    os.system("raspistill -t " + countdown + " -o " + image + " -w " + \
              config.imgw + " -h " + config.imgh + " -p " + dims)
    return image

def send_picture(uid,image_file):
	
	if os.path.isfile(image_file):
            print("send_picture(" + uid + "," + image_file + ")")
	    os.system("curl -s -L -u tmwcolin:waitalittle -F \"photo=@/home/pi/pi-booth/app/" + \
                      image_file + ";type=application/octet-stream;\" -F \"guid=" + \
                      str(uid) + "\" http://gps.tmw.co.uk/ajax/photobooth.php")
	else:
	    print("Error: File not found: " + image_file)
	

	#TODO: create preferences file and write to that instead of volatile var for image_count
	
	#294 = Roo's guid on the intranet.
