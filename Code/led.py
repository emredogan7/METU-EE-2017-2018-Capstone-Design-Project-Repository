import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

pin_output = #18
pin_input = #16

GPIO.setup(pin_output,GPIO.OUT)
GPIO.output(pin_output,GPIO.HIGH)
GPIO.setup(pin_input, GPIO.IN)
state = GPIO.input(pin_input)
print (state)
if state :
    filename = "mode.txt"
    file = open(filename, "w")
    mode = "Master"
    file.write(mode)
    file.close()
    print ("Red is on, Master Mode!")
else:
    filename = "mode.txt"
    file = open(filename, "w")
    mode = "Slave"
    file.write(mode)
    file.close()
    print ("Yellow is on, Slave Mode!")
time.sleep(5)
GPIO.output(pin_output,GPIO.LOW)
