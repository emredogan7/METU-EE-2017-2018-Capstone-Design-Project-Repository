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
	left_dist  = measure_distance(Trig_left,Echo_left)
    total      = right_dist + left_dist

    if ( front_dist < 12 and total > 25 ):
        if right_dist > left_dist :
			while (front_dist < 30):
				motor_adj(10, 10, 0, 1)
				time.sleep(0.05)
			print ("A")
        else:
			while (front_dist < 30):
				motor_adj(10, 10, 1, 0)
				time.sleep(0.05)
            print ("B")

		motor_adj(10, 10, 1, 1)
		time.sleep(0.3)


    else:
        if total > 25 :
            if right_dist > left_dist :
                if left_dist > 10 :
                    motor_adj(10,8,1,1)
                else:
                    motor_adj(8,10,1,1)
            else:
                if right_dist > 10 :
                    motor_adj(8,10,1,1)
                else:
                    motor_adj(10,8,1,1)
        else:
            if right_dist > 10 :
                motor_adj(8,10,1,1)
            else:
                motor_adj(10,8,1,1)
