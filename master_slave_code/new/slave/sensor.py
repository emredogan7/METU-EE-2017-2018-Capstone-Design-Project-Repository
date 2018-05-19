import time
import RPi.GPIO as GPIO
GPIO.cleanup()

mode=GPIO.getmode()
GPIO.setmode(GPIO.BCM)


def set_distance_hw(TRIG,ECHO):

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

def measure_distance(TRIG,ECHO):
  GPIO.output(TRIG, False)
  time.sleep(0.1)

  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)

  count=time.time()
  while GPIO.input(ECHO)==0 and time.time()-count<0.1:
    pulse_start = time.time()

  pulse_end = time.time()
  count=time.time()
  while GPIO.input(ECHO)==1 and time.time()-count<0.1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start

  distance = pulse_duration * 17150
  distance = round(distance, 2)
  """
  if   TRIG == 19:
      print ("Front dist :")
  elif TRIG == 21:
      print ("Right dist :")
  elif TRIG == 9:
      print ("left dist :")
  else:
      print ("back dist :")
  print ( distance )
  print ("\n")
  """
  return distance
