import RPi.GPIO as gpio

# Setup
import atexit
import sys
import time
import RPi.GPIO as GPIO

mode=GPIO.getmode()
GPIO.setmode(GPIO.BCM)

TRIG_1 = 21
ECHO_1 = 20

TRIG_2 = 19
ECHO_2 = 26

#TRIG_3 = 23
#ECHO_3 = 24


def set_distance_hw(TRIG,ECHO):
    
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    
def measure_distance(TRIG,ECHO):
  GPIO.output(TRIG, False)
  #print ("Olculuyor...")
  time.sleep(0.5)

  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)

  while GPIO.input(ECHO)==0:
    pulse_start = time.time()

  while GPIO.input(ECHO)==1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start

  distance = pulse_duration * 17150
  distance = round(distance, 2)
  if TRIG == 19:
      print ("Front dist :")
  else:
      print ("Right dist :")
  print ( distance )
  print ("\n")
  return distance
    


#measure_distance(TRIG_3,ECHO_3)
