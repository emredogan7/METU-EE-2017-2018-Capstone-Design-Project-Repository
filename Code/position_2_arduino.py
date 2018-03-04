from RPIO import PWM

#This function sends position information to arduino via PWM

def Current_Position(Dist_2_Left, Dist_2_Right):
    Current_Position = ( Dist_2_Right - Dist_2_Left) / 2.0
    return Current_Position #Right is negative whereas left is positive

def Duty_Cycle_Percantage(Current_Position):
    Duty_Cycle_Percantage = ( Current_Position * 10 ) + 50
    return Duty_Cycle_Percantage

def Pulse_Time(Duty_Cycle_Percantage):
    Pulse_Time = 200 * Duty_Cycle_Percantage
    return int(Pulse_Time)
print Pulse_Time(Duty_Cycle_Percantage(Current_Position(7,3)))



servo = PWM.Servo()
servo.set_servo(17, 2000)
servo.stop_servo(17)
#Example of using PWM.Servo (with the default subcycle time of
#20ms and default pulse-width increment granularity of 10us):
