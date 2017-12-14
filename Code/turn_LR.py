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

def turnleft(x):
    GPIO.output(FwdL, GPIO.HIGH)
    GPIO.output(FwdR, GPIO.LOW)
    print("Moving Forward")
    time.sleep(x)
    GPIO.output(FwdL, GPIO.LOW)
    GPIO.output(FwdR, GPIO.HIGH)

def turnright(x):
    GPIO.output(BwdL, GPIO.HIGH)
    GPIO.output(BwdR, GPIO.LOW)
    print("Moving Backward")
    time.sleep(x)
    GPIO.output(BwdL, GPIO.LOW)
    GPIO.output(BwdR, GPIO.HIGH)

def forward(x):
    GPIO.output(FwdL, GPIO.HIGH)
    GPIO.output(FwdR, GPIO.HIGH)
    print("Moving Forward")
    time.sleep(x)
    GPIO.output(FwdL, GPIO.LOW)
    GPIO.output(FwdR, GPIO.LOW)

def reverse(x):
    GPIO.output(BwdL, GPIO.HIGH)
    GPIO.output(BwdR, GPIO.HIGH)
    print("Moving Backward")
    time.sleep(x)
    GPIO.output(BwdL, GPIO.LOW)
    GPIO.output(BwdR, GPIO.LOW)


while (1):
    
    turnleft(0.6)

    turnright(0.3)
GPIO.cleanup()