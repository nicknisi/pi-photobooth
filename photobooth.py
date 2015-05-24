import RPi.GPIO as GPIO
import atexit
from time import sleep, strftime
import subprocess
import pygame
import os
import socket

# variables
transform_x = 800
transform_y = 480
offset_x = 0
offset_y = 0

led_pin = 4
button_pin = 17
halt_pin = 4
network_pin = 23
real_path = os.path.dirname(os.path.realpath(__file__))
temp_dir = real_path + '/.photos'
photos_dir = real_path + '/photos'


GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT);
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection
GPIO.setup(halt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection

# setup rgb led
red_pin = 12
green_pin = 16
blue_pin = 18

GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.setup(network_pin, GPIO.OUT)

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

def reboot():
	cleanup()
	sleep(2)
	os.system('sudo reboot')

def is_connected():
	try:
		host = socket.gethostbyname('www.google.com')
		s = socket.create_connection((host, 80), 2)
		return True
	except:
		pass
	return False

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

def init_pygame():
	pygame.init()
	size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
	pygame.display.set_caption('Photo Booth Pics')
	pygame.mouse.set_visible(False)
	return pygame.display.set_mode(size, pygame.FULLSCREEN)

def show_image(image_path):
	screen = init_pygame()
	img = pygame.image.load(image_path)
	img = pygame.transform.scale(img,(transform_x,transform_y))
	screen.blit(img, (offset_x, offset_y))
	pygame.display.flip()

def snap():
	pics = 0
	now = strftime('%Y-%m-%d-%H:%M:%S')

	while pics < 4:
		print('pose!')
		show_image(real_path + '/images/pose.png')
		sleep(1)
		blink(yellow, 5, 0.4)
		blink(yellow, 5, 0.1)
		print('SNAP')
		setcolor(red)
		filename = temp_dir + '/photo-' + now + '-' + `pics` + '.jpg'
		print('filename: ' + filename)
		gpout = subprocess.check_output('gphoto2 --capture-image-and-download --keep --filename ' + filename, stderr=subprocess.STDOUT, shell=True)
		print(gpout)
		if "ERROR" not in gpout:
			print('SUCCESS!')
			show_image(filename)
			sleep(2)
			pics += 1
		else:
			print(gpout)
			blink([80, 0, 80], 5, 0.5)
		# sleep(0.5)
	# TODO: upload LED
	print('assembling photo strip')
	show_image(real_path + '/images/waiting.png')
	photo = real_path + '/photos/' + now + '.jpg'
	assembleout = subprocess.check_output('sudo ' + real_path + '/assemble_and_upload ' + photo, shell=True)
	print(assembleout)
	show_image(photo)
	sleep(3)
	setcolor(green)
	show_image(real_path + '/images/ready.png')


# blink(red, 2, 1)
setcolor(green)

# GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=snap, bouncetime=300)

# turn on the red light if we're not connected
GPIO.output(network_pin, not is_connected())

show_image(real_path + '/images/ready.png')

while True:
	if (GPIO.input(button_pin) != 1):
		snap()
		sleep(1)
	elif (GPIO.input(halt_pin) != 1):
		reboot()
