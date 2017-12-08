import RPi.GPIO as gpio

# Setup
import atexit

a_en = 7
a_in1 = 13
a_in2 = 15

b_en = 12
b_in1 = 18
b_in2 = 22

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(a_en, gpio.OUT)
gpio.setup(a_in1, gpio.OUT)
gpio.setup(a_in2, gpio.OUT)
gpio.setup(b_en, gpio.OUT)
gpio.setup(b_in1, gpio.OUT)
gpio.setup(b_in2, gpio.OUT)

# Have the in pins be off initially, except for the enable pins
gpio.output(a_in1, False)
gpio.output(a_in2, False)
gpio.output(b_in1, False)
gpio.output(b_in2, False)
gpio.output(a_en, True)
gpio.output(b_en, True)


# Turn off all pins when the program quits
def disable():
    gpio.output(a_in1, False)
    gpio.output(a_in2, False)
    gpio.output(b_in1, False)
    gpio.output(b_in2, False)
    gpio.output(a_en, False)
    gpio.output(b_en, False)
atexit.register(disable)


# Move functions
def move_a(forward):
    gpio.output(a_in1, forward)
    gpio.output(a_in2, not forward)

def move_b(forward):
    gpio.output(b_in1, forward)
    gpio.output(b_in2, not forward)

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
    gpio.output(a_in1, False)
    gpio.output(a_in2, False)
    gpio.output(b_in1, False)
    gpio.output(b_in2, False)
