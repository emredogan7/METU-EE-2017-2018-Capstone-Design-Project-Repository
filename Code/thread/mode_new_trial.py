import RPi.GPIO as GPIO
import time

class Mode:
    'Description of the code'
    Mode = 0 # 0 for master

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        pin_output = #18
        pin_input = #16

        GPIO.setup(pin_output,GPIO.OUT)

        GPIO.setup(pin_input, GPIO.IN)


        print "Check robot's mode! \n"

    def check(self):
        GPIO.output(pin_output,GPIO.HIGH)
        state = GPIO.input(pin_input)
        if state :
            Mode.Mode = 0
        else:
            Mode.Mode = 1
        GPIO.output(pin_output,GPIO.LOW)

    def is_slave(self):
        return Mode.Mode
