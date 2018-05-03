from sensor import set_distance_hw
from sensor import measure_distance
from motor  import motor_adj
import time


Trig_front = 19
Echo_front = 26
Trig_right = 21
Echo_right = 20
Trig_left = 9
Echo_left = 11
#first integers       = speed
#second integers = direction (1 forward, 0 backward)

set_distance_hw(Trig_front,Echo_front)
set_distance_hw(Trig_right,Echo_right)
set_distance_hw(Trig_left,Echo_left)

while ( 1 ) :
    
    front_dist = measure_distance(Trig_front,Echo_front)
    right_dist = measure_distance(Trig_right,Echo_right)
	left_dist = measure_distance(Trig_left,Echo_left)
    
    if (front_dist <= 12):
        if right_dist > 20 :
			while (front_dist < 30):
				motor_adj(10, 10, 0, 1)
				time.sleep(0.05)
			print ("A")
        elif right_dist < 20:
			while (front_dist < 30):
				motor_adj(10, 10, 1, 0)
				time.sleep(0.05)
            print ("B")
		else:
			motor_adj(10, 10, 1, 1)
        
		motor_adj(10, 10, 1, 1)
		time.sleep(0.3)
		
        
    else:
		dist_difference = abs(right_dist - left_dist)
        if (dist_difference < 10) and (dist_difference > 9)
			motor_adj(10, 10, 1, 1)
			
		else:
			if right_dist > left_dist
				motor_adj(8, (8+dist_difference), 1, 1)
			elif right_dist < left_dist
				motor_adj((8+dist_difference), 8, 1, 1)
		"""	
		if right_dist <= 11:
            motor_adj(40,20,1,1)
            print ("C")
        elif right_dist >= 13:
            motor_adj(20,40,1,1)
            print ("D")
        else :
            motor_adj(30,30,1,1)
            print ("E")
        """ 
    
    
    
