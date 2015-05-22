import RPi.GPIO as GPIO
import atexit
from time import sleep
import subprocess

led_pin = 4
button_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT);
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection

# setup rgb led
red_pin = 12
green_pin = 16
blue_pin = 18

GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)

# setup the colors
freq = 100 # hz
RED = GPIO.PWM(red_pin, freq)
RED.start(0)
GREEN = GPIO.PWM(green_pin, freq)
GREEN.start(0)
BLUE = GPIO.PWM(blue_pin, freq)
BLUE.start(0)

# colors
red = [60, 0, 0]
green = [0, 60, 0]
yellow = [60, 60, 0]


def cleanup():
	print('Closing...')
	GPIO.cleanup()
atexit.register(cleanup)

def setcolor(color):
	RED.ChangeDutyCycle(color[0])
	GREEN.ChangeDutyCycle(color[1])
	BLUE.ChangeDutyCycle(color[2])

def blankcolor():
	setcolor([0, 0, 0])

def blink(color, numTimes, speed):
	for i in range(0, numTimes):
		setcolor(color)
		sleep(speed)
		blankcolor()
		sleep(speed)

def snap(colo):
	pics = 0
	while pics < 4:
		print('pose!')
		sleep(1.5)
		blink(yellow, 5, 0.4)
		blink(yellow, 5, 0.1)
		print('SNAP')
		setcolor(red)
		gpout = subprocess.check_output('gphoto2 --capture-image-and-download --keep --filename /home/pi/code/pi-photobooth/.photos/photo%H%M%S.jpg', stderr=subprocess.STDOUT, shell=True)
		print(gpout)
		if "ERROR" not in gpout:
			print('SUCCESS!')
			pics += 1
		else:
			print(gpout)
		# sleep(0.5)
	# TODO: upload LED
	print('assembling photo strip')
	assembleout = subprocess.check_output('sudo /home/pi/code/pi-photobooth/assemble_and_upload', shell=True)
	print(assembleout)
	setcolor(green)


blink(red, 2, 1)
setcolor(green)

GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=snap, bouncetime=300)

while True:
	sleep(0.2)

