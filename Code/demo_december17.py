import sys
import time
import RPi.GPIO as GPIO

mode=GPIO.getmode()

GPIO.cleanup()

FwdL=26
BwdL=20
FwdR=19
BwdR=16
sleeptime=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(FwdL, GPIO.OUT)
GPIO.setup(FwdR, GPIO.OUT)
GPIO.setup(BwdL, GPIO.OUT)
GPIO.setup(BwdR, GPIO.OUT)

def forward(x):
    GPIO.output(FwdL, GPIO.HIGH)
    GPIO.output(FwdR, GPIO.LOW)
    print("Moving Forward")
    time.sleep(x)
    GPIO.output(FwdL, GPIO.LOW)
    GPIO.output(FwdR, GPIO.HIGH)

def backward(x):
    GPIO.output(BwdL, GPIO.HIGH)
    GPIO.output(BwdR, GPIO.LOW)
    print("Moving Backward")
    time.sleep(x)
    GPIO.output(BwdL, GPIO.LOW)
    GPIO.output(BwdR, GPIO.HIGH)

def turnleft(x):
    GPIO.output(FwdL, GPIO.HIGH)
    GPIO.output(FwdR, GPIO.HIGH)
    print("Gemi Sola Çekiyor Kuna")
    time.sleep(x)
    GPIO.output(FwdL, GPIO.LOW)
    GPIO.output(FwdR, GPIO.LOW)

def turnright(x):
    GPIO.output(BwdL, GPIO.HIGH)
    GPIO.output(BwdR, GPIO.HIGH)
    print("Gemi Sağa Çekiyor Kuna")
    time.sleep(x)
    GPIO.output(BwdL, GPIO.LOW)
    GPIO.output(BwdR, GPIO.LOW)
    

#Sensor part
def frw_s(): 
    TRIG = 23
    ECHO = 24

    #print ("HC-SR04 mesafe sensoru")

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    while True:

      GPIO.output(TRIG, False)
      #print ("Olculuyor...")
      time.sleep(0.00001)

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

      if distance < 10:
          print ("Distance is less than 15cm")
          return 0;
      else:
          print ("No problem.")
          return 1;
#Mesafe az kaldıysa 0 dönecek ki iften çıksın!


while (1):
    
    if frw_s():
        forward(1)
    else:
        backward(1)
    
    #reverse(1)
    
   ## turnleft(1)

    #turnright(1)
GPIO.cleanup()                                                                                    