from sensor import set_distance_hw
from sensor import measure_distance
from motor  import motor_adj
import time


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
    
    
    
    
    if front_dist <= 10:
        if right_dist > 20 :
            motor_adj(25,25,0,1)
            print ("A")
        else:
            motor_adj(25,25,1,0)
            print ("B")
        time.sleep(0.75)
        
    else:
        if right_dist <= 11:
            motor_adj(40,20,1,1)
            print ("C")
        elif right_dist >= 13:
            motor_adj(20,40,1,1)
            print ("D")
        else :
            motor_adj(30,30,1,1)
            print ("E")
         
    
    
    

