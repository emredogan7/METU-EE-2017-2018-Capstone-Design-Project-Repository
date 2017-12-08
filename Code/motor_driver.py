import sys
import time
import RPi.GPIO as GPIO
"""
#sense
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#sense_end
"""
from sens import frw_s;
from sens import back_s;
from sens import right_s;
from sens import left_s;

mode=GPIO.getmode()

GPIO.cleanup()

Forward=26
Backward=20
sleeptime=1

import atexit

a_en = 7
a_in1 = 13
a_in2 = 15

b_en = 12
b_in1 = 18
b_in2 = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(a_en, GPIO.OUT)
GPIO.setup(a_in1, GPIO.OUT)
GPIO.setup(a_in2, GPIO.OUT)
GPIO.setup(b_en, GPIO.OUT)
GPIO.setup(b_in1, GPIO.OUT)
GPIO.setup(b_in2, GPIO.OUT)


# Have the in pins be off initially, except for the enable pins
GPIO.output(a_in1, False)
GPIO.output(a_in2, False)
GPIO.output(b_in1, False)
GPIO.output(b_in2, False)
GPIO.output(a_en, True)
GPIO.output(b_en, True)


# Turn off all pins when the program quits
def disable():
    GPIO.output(a_in1, False)
    GPIO.output(a_in2, False)
    GPIO.output(b_in1, False)
    GPIO.output(b_in2, False)
    GPIO.output(a_en, False)
    GPIO.output(b_en, False)
atexit.register(disable)


# Movement functions of motors
# a: motor1, b:motor2
def move_a(forward):
    GPIO.output(a_in1, forward)
    GPIO.output(a_in2, not forward)

def move_b(forward):
    GPIO.output(b_in1, forward)
    GPIO.output(b_in2, not forward)

def move_forward():
    move_a(True)
    move_b(True)

def move_backward():
    move_a(False)
    move_b(False)

def rotate_left():
    move_a(True)
    move_b(False)

def rotate_right():
    move_a(False)
    move_b(True)

def stop():
    GPIO.output(a_in1, False)
    GPIO.output(a_in2, False)
    GPIO.output(b_in1, False)
    GPIO.output(b_in2, False)




while (True):
    
    forward=frw_s();   #Will return "1" if no obstacle ahead.
    backward=back_s(); #will return "1" if no obstacle behind.
    left=left_s();     #will return "1" if no obstacle left.
    right=right_s();   #will return "1" if no obstacle right.
    
    #the order in the following code block is important as the standard priority is to turn right as possible as.
    
    #decision 
    if forward ==0:
        move_forward(); 
    elif right ==0:      
        rotate_right(); 
    elif left ==0:
        rotate_left();
    else :
        move_backward();
        


GPIO.cleanup()



