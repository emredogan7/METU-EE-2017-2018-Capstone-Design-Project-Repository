import RPi.GPIO as GPIO

import RPi.GPIO as IO          

import time  

mode = GPIO.getmode()
GPIO.setmode( GPIO.BCM )

IO.setwarnings(False)          

IO.setmode (IO.BCM)         


GPIO.setup(6 ,GPIO.OUT )
GPIO.setup(5 ,GPIO.OUT )

GPIO.output(6,True)
GPIO.output(5,False)


GPIO.setup(7 ,GPIO.OUT )
GPIO.setup(8 ,GPIO.OUT )

GPIO.output(7,False)
GPIO.output(8,True)

                
IO.setup(19,IO.OUT)           
IO.setup(12,IO.OUT)

pwm_0 = IO.PWM(19,100)
pwm_1 = IO.PWM(12,100)                    

pwm_0.start(0)                              
pwm_1.start(0)                              

while 1:                               

    for x in range (50):                   
        pwm_0.ChangeDutyCycle(x)               
	pwm_1.ChangeDutyCycle(x)               
        time.sleep(0.1)                     
      
    for x in range (50):                          
        pwm_0.ChangeDutyCycle(50-x)               
	pwm_1.ChangeDutyCycle(50-x)               
        time.sleep(0.1)                          
