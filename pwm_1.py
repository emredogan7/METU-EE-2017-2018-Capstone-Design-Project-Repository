import RPi.GPIO as GPIO

from RPIO import PWM


servo = PWM.servo()
mode = GPIO.getmode()
GPIO.setmode( GPIO.BCM )

GPIO.setup( ,GPIO.OUT )
GPIO.setup( ,GPIO.OUT )

GPIO.output(,True)
GPIO.output(,True)


while True:
    for i in range (100):
        servo.set_servo( , 2000 )
        servo.set_servo( , 2000 )
    for i in range (100):
        servo.set_servo( , 1000 )
        servo.set_servo( , 1000 )
    for i in range (100):
        servo.set_servo( , 0 )
        servo.set_servo( , 0 )

servo.stop_servo(17)
