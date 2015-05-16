import RPi.GPIO as GPIO
import atexit
from time import sleep

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
    print('blink')
    blink(led_pin, 4, 0.2)
    print('TODO: take pic')

blink(led_pin, 2, 1)

GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=snap, bouncetime=300)

while True:
    # input_state = GPIO.input(button_pin)
    # if input_state == False:
    #     print('button pressed')
    sleep(0.2)
