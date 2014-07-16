import sys, os, time
import RPIO


flash_pin = 4
RPIO.setmode(RPIO.BCM)
RPIO.setup(flash_pin, RPIO.OUT)
RPIO.output(flash_pin, True) #turn off pin


def flash_on():
	RPIO.output(flash_pin, False) 
	
def flash_off():
	RPIO.output(flash_pin, True)

def loop():
	flash_on()
	time.sleep(20)
	flash_off()
	RPIO.cleanup()
	
if __name__ == '__main__':
	loop()
