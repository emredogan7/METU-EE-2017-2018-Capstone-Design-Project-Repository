import RPi.GPIO as GPIO
import time

GPIO.setmode( GPIO.BCM )

VCC         = 18
Green_LED   = 14
Red_LED     = 15
Read_Switch = 17

GPIO.setup(VCC          , GPIO.OUT)
GPIO.setup(Green_LED    , GPIO.OUT)
GPIO.setup(Red_LED      , GPIO.OUT)

GPIO.setup(Read_Switch  , GPIO.IN )

#Turn on power
GPIO.output(VCC      , 1)

#Emitting yellow
GPIO.output(Green_LED, 0)
GPIO.output(Red_LED  , 0)
print ("In Halt mode!")
time.sleep(2)
print ("I'm awake,now!")

state = GPIO.input(Read_Switch)

# state == 1 => master
# state == 0 => slave

if state == 1 :
    GPIO.output(Red_LED  , 1)
    print ("Master Mode -> green led is turned on!")
else:
    GPIO.output(Green_LED, 1)
    print ("Slave Mode -> red led is turned on!"   )

