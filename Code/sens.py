

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#frw_s returns "1" if distance is less than 15 cm
#else returns "0"

#back_s returns "1" if distance is less than 15 cm
#else returns "0"

#right_s returns "1" if distance is less than 25 cm
#else returns "0"

#left_s returns "1" if distance is  less than 25 cm
#else returns "0"

def frw_s(): 
    TRIG = 23
    ECHO = 24

    print ("HC-SR04 mesafe sensoru")

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    while True:

      GPIO.output(TRIG, False)
      print ("Olculuyor...")
      time.sleep(2)

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

      if distance < 15:
        print ("Distance is less than 15cm")
        return 1;
      else:
        print ("No problem.")
        return 0;



def back_s(): 
    TRIG = 23
    ECHO = 24

    print ("HC-SR04 mesafe sensoru")

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    while True:

      GPIO.output(TRIG, False)
      print ("Olculuyor...")
      time.sleep(2)

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

      if distance < 15:
        print ("Distance is less than 15cm")
        return 1;
      else:
        print ("No problem.")
        return 0;





def left_s(): 
    TRIG = 23
    ECHO = 24

    print ("HC-SR04 mesafe sensoru")

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    while True:

      GPIO.output(TRIG, False)
      print ("Olculuyor...")
      time.sleep(2)

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

      if distance < 25:
        print ("Distance is much more than 25cm")
        return 1;
      else:
        print ("No problem.")
        return 0;




def right_s(): 
    TRIG = 23
    ECHO = 24

    print ("HC-SR04 mesafe sensoru")

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    while True:

      GPIO.output(TRIG, False)
      print ("Olculuyor...")
      time.sleep(2)

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

      if distance < 25:
        print ("Distance is much more than 25cm")
        return 1;
      else:
        print ("No problem.")
        return 0;
