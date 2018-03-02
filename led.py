import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.HIGH)

pin = 16
GPIO.setup(pin, GPIO.IN)
state = GPIO.input(pin)

if state :
filename = "mode.txt"
file = open(filename, "w")
mode = "Master"
file.write(mode)
file.close()
print "Red is on, Master Mode!"
else:
filename = "mode.txt"
file = open(filename, "w")
mode = "Slave"
file.write(mode)
file.close()
print "Yellow is on, Slave Mode!"
