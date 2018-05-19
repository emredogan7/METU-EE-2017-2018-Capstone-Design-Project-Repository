import RPi.GPIO as GPIO

import RPi.GPIO as IO          

import time  

mode = GPIO.getmode()
GPIO.setmode( GPIO.BCM )

IO.setwarnings(False)          

IO.setmode (IO.BCM)         


GPIO.setup(6 ,GPIO.OUT )
GPIO.setup(5 ,GPIO.OUT )




GPIO.setup(7 ,GPIO.OUT )
GPIO.setup(8 ,GPIO.OUT )



                
IO.setup(13,IO.OUT)           
IO.setup(12,IO.OUT)

pwm_0 = IO.PWM(13,100)
pwm_1 = IO.PWM(12,100)




def motor_adj( speed_right, speed_left, dir_right, dir_left):

    pwm_0.start(0)                              
    pwm_1.start(0)
    
    dir_right_not = 1 - dir_right
    dir_left_not  = 1 - dir_left
    
    GPIO.output(6,dir_right)
    GPIO.output(5,dir_right_not)
    
    GPIO.output(8,dir_left_not)
    GPIO.output(7,dir_left)
    
    
    
    pwm_0.ChangeDutyCycle(speed_right) 
    pwm_1.ChangeDutyCycle(speed_left)


if __name__ == "__main__":
    
    motor_adj(50,0,1,1)