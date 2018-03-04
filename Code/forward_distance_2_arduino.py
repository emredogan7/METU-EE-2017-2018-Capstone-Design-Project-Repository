from RPIO import PWM

#This function sends Forward Distance information to arduino via PWM



# This function calculates how close the robot to he wall
# 40.0 is the nearest whereas 0.0 is the longest distance
def Proximity(Forward_Dist):
    Proximity = ( ( Forward_Dist ) * -1 ) + 40.0
    if Proximity < 0 :
	Proximity = 0.0
    return Proximity 

def Duty_Cycle_Percantage(Proximity):
    Duty_Cycle_Percantage = ( Proximity * 2.5 )
    return Duty_Cycle_Percantage

def Pulse_Time(Duty_Cycle_Percantage):
    Pulse_Time = 200 * Duty_Cycle_Percantage
    return int(Pulse_Time)

print Pulse_Time(Duty_Cycle_Percantage(Proximity(15)))



servo = PWM.Servo()
servo.set_servo(17, 2000)
servo.stop_servo(17)
#Example of using PWM.Servo (with the default subcycle time of
#20ms and default pulse-width increment granularity of 10us):
