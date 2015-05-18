import RPi.GPIO as GPIO
import atexit
from time import sleep
import subprocess

led_pin = 4
button_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT);
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection

def cleanup():
	print('Closing...')
	GPIO.cleanup()
atexit.register(cleanup)

def blink(led, numTimes, speed):
	for i in range(0, numTimes):
		GPIO.output(led, True)
		sleep(speed)
		GPIO.output(led, False)
		sleep(speed)

def snap(pressed):
	pics = 0
	while pics < 4:
		print('pose!')
		sleep(1.5)
		blink(led_pin, 5, 0.4)
		blink(led_pin, 5, 0.1)
		print('SNAP')
		gpout = subprocess.check_output('gphoto2 --capture-image-and-download --keep --filename /home/pi/code/pi-photobooth/.photos/photo%H%M%S.jpg', stderr=subprocess.STDOUT, shell=True)
		print(gpout)
		if "ERROR" not in gpout:
			print('SUCCESS!')
			pics += 1
		else:
			print(gpout)
		# sleep(0.5)
	# TODO: upload LED
	assembleout = subprocess.check_output('sudo /home/pi/code/pi-photobooth/assemble_and_upload', shell=True)
	print(assembleout)


blink(led_pin, 2, 1)

GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=snap, bouncetime=300)

while True:
	# input_state = GPIO.input(button_pin)
	# if input_state == False:
	#	  print('button pressed')
	sleep(0.2)
