import RPi.GPIO as GPIO
import atexit
from time import sleep, strftime
import subprocess
import pygame
import os
import socket
import threading
import PIL
from PIL import Image
import shutil
import cups

PIC_COUNT = 4

# Variables:
#   Screen size:
#transform_x = 1680
#transform_y = 1050
transform_x = 1920
transform_y = 1080
offset_x = 0
offset_y = 0

#    GPIO:
led_pin = 4
button_pin = 17
halt_pin = 4
network_pin = 23
real_path = os.path.dirname(os.path.realpath(__file__))
temp_dir = real_path + '/.photos'
raw_dir = real_path + '/raws'
photos_dir = real_path + '/combined_photos'


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

def set_interval(func, sec):
	def func_wrapper():
		set_interval(func, sec)
		func()
	t = threading.Timer(sec, func_wrapper)
	t.daemon = True
	t.start()
	return t

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

# Print the photo
def printPhoto(photo):
        print('Printing')

        conn = cups.Connection()
        printers = conn.getPrinters()
        printer_name = printers.keys()[0]
        conn.printFile(printer_name, photo,"TITLE",{})


def combineImages(photo):
    #displayStatus('Please wait. Processing Images')
                            
        # Do the merging
        blankImage = Image.open(real_path + '/images/blank.jpg')

        image1 = Image.open(temp_dir + '/image0.jpg')        
        #image1 = image1.resize((600,400),PIL.Image.ANTIALIAS)
        #blankImage.paste(image1, (190,190))
        blankImage.paste(image1, (160,160))

        image2 = Image.open(temp_dir + '/image1.jpg')        
        #image2 = image2.resize((600,400),PIL.Image.ANTIALIAS)
        #blankImage.paste(image2, (810,190))
        blankImage.paste(image2, (840,160))

        image3 = Image.open(temp_dir + '/image2.jpg')        
        #image3 = image3.resize((600,400),PIL.Image.ANTIALIAS)
        #blankImage.paste(image3, (190,610))
        blankImage.paste(image3, (160,630))

        image4 = Image.open(temp_dir + '/image3.jpg')        
        #image4 = image4.resize((600,400),PIL.Image.ANTIALIAS)
        #blankImage.paste(image4, (810,610))
        blankImage.paste(image4, (840,630))

        blankImage.save(photo, quality=100)

def snap():
	pics = 0
	now = strftime('%Y-%m-%d-%H:%M:%S')
        shutil.rmtree(temp_dir)
        if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

	while pics < PIC_COUNT:
		print('pose!')
		show_image(real_path + '/images/pose.jpg')
		#sleep(1)
		blink(yellow, 5, 0.4)
		blink(yellow, 5, 0.1)
		print('SNAP')
		setcolor(red)
		filename = raw_dir + '/photo-' + now + '-' + `pics` + '.cr2'
		outFileName = temp_dir + '/image' + `pics` + '.jpg'
		print('filename: ' + filename)
		gpout = subprocess.check_output('gphoto2 --capture-image-and-download --keep --filename ' + filename, stderr=subprocess.STDOUT, shell=True)
                #ufrawCmd = "ufraw-batch --out-type jpg %s --output=%s --size=600,400 --silent" % (filename, outFileName)
                ufrawCmd = "ufraw-batch --out-type jpg %s --output=%s --size=640,480 --silent" % (filename, outFileName)
                print ufrawCmd
                #subprocess.Popen(["ufraw-batch","--out-type","jpg",filename,"--output=outFileName","--size=600,400"])
                p = subprocess.Popen(ufrawCmd.split())
		print(gpout)
		if "ERROR" not in gpout:
			print('SUCCESS!')
			show_image(filename)
			sleep(5)
			pics += 1
		else:
                        print ('ERROR!')
		        print(gpout)
			blink([80, 0, 80], 5, 0.5)
		# sleep(0.5)
	# TODO: upload LED
	print('assembling photo strip')
	show_image(real_path + '/images/waiting.jpg')
        sleep (5)
	photo = photos_dir + '/' + now + '.jpg'
        #print ('ufraw:')
        #os.system("ufraw-batch --out-type jpg " + temp_dir + "/*.cr2")
        p.wait()
        combineImages(photo)
	#assembleout = subprocess.check_output('sudo ' + real_path + '/assemble_and_upload ' + photo, shell=True)
	#print(assembleout)
	show_image(photo)
        printPhoto(photo)
	sleep(10)
	setcolor(green)
	show_image(real_path + '/images/ready.jpg')

def check_connectivity():
	# turn on the red light if we're not connected
	GPIO.output(network_pin, not is_connected())

set_interval(check_connectivity, 60)


# blink(red, 2, 1)
setcolor(green)

# GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=snap, bouncetime=300)

show_image(real_path + '/images/ready.jpg')

while True:
	if (GPIO.input(button_pin) != 1):
		snap()
		sleep(1)
	elif (GPIO.input(halt_pin) != 1):
                print("something")
		#reboot()
