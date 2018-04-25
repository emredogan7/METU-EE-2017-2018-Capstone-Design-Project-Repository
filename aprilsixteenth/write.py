from sensor import set_distance_hw
from sensor import measure_distance
import serial
import time
ser = serial.Serial('/dev/ttyUSB0',9600)
mahmut = 9191

Trig_front = 19
Echo_front = 26
Trig_right = 21
Echo_right = 20
#first integers       = speed
#second integers = direction (1 for forward, 0 for backward)

set_distance_hw(Trig_front,Echo_front)
set_distance_hw(Trig_right,Echo_right)    
while ( 1 ) :
    
    front_dist = measure_distance(Trig_front,Echo_front)
    right_dist = measure_distance(Trig_right,Echo_right)
    
    if front_dist <= 8:
        if right_dist > 20 :
            mahmut = 6061
        else:
            mahmut = 6160
                
    else:
        if right_dist <= 4:
            mahmut = 9181
        elif right_dist >= 6:
            mahmut = 9181
        else :
            mahmut = 9181
            
    print ( mahmut )
    
    ser.write( str(mahmut).encode() );
    time.sleep(0.01);
    
    if front_dist <= 8:
        time.sleep(0.01);
    
