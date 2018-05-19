from sensor import set_distance_hw
from sensor import measure_distance
from motor  import motor_adj
import time,cv2
from angle import find_angle

Trig_front = 19
Echo_front = 26

Trig_right = 21
Echo_right = 20

Trig_left  = 9
Echo_left  = 11

Trig_back  = 22
Echo_back  = 27

set_distance_hw(Trig_front,Echo_front)
set_distance_hw(Trig_right,Echo_right)
set_distance_hw(Trig_left ,Echo_left )
set_distance_hw(Trig_back ,Echo_back )

state  = 2
dist_1 = 32.5 #state 2
dist_2 = 27.0 #state 4
dist_3 = 45.0 #state 6

#adjust the motor percentage
# duz yonu normalde aracin arkasi
def obstacle(right_dist,left_dist):
    motor_adj(0, 0, 0, 1)
    time.sleep(3)
    if right_dist > left_dist:
        motor_adj(20, 20, 0, 1)
        #time.sleep(0.8)
    else:
       motor_adj(20, 20, 1, 0)
    time.sleep(1)
    motor_adj(0, 0, 1, 1)
    time.sleep(3)

def obstacle_inv(right_dist,left_dist):
    motor_adj(0, 0, 0, 1)
    time.sleep(3)
    if left_dist  > right_dist:
        motor_adj(20, 20, 0, 1)
        #time.sleep(0.8)
    else:
        motor_adj(20, 20, 1, 0)
    time.sleep(1)
    motor_adj(0, 0, 1, 1)
    time.sleep(3)

#master a gore duz, araca gore ters
def bang_bang(right_dist,left_dist,total):
    if total > 25 :
        if right_dist > left_dist:
            if left_dist > 10.5:
                motor_adj(15,20,0,0)

            else:
                motor_adj(20,15,0,0)

        else:
            if right_dist > 10.5:
                motor_adj(20,15,0,0)

            else:
                motor_adj(15,20,0,0)

    else:
        if right_dist > ( total / 2 ):
            motor_adj(20,15,0,0)

        else:
            motor_adj(15,20,0,0)

def bang_bang_inv(right_dist,left_dist,total):
    if total > 25 :
        if left_dist > right_dist:
            if  right_dist > 10.5:
                motor_adj(20,15,1,1)

            else:
                motor_adj(15,20,1,1)

        else:
            if left_dist > 10.5:
                motor_adj(15,20,1,1)

            else:
                motor_adj(20,15,1,1)

    else:
        if left_dist > ( total / 2 ):
            motor_adj(15,20,1,1)

        else:
            motor_adj(20,15,1,1)
"""
def wait():
    motor_adj(0, 0, 1, 1)
    time.sleep(5)


while True:
    cap = cv2.VideoCapture(0)
    print "Angle_cam is being adjusted"
    if ( cap.isOpened() ) :  # check if we succeeded
        cap.set( cv2.CAP_PROP_FRAME_WIDTH,  640 )
        cap.set( cv2.CAP_PROP_FRAME_HEIGHT, 480 )
        break
"""
while True:
    # master orientation = measure_distance(robots original orientation)
    back_dist  = measure_distance(Trig_front,Echo_front)
    left_dist  = measure_distance(Trig_right,Echo_right)
    right_dist = measure_distance(Trig_left ,Echo_left )
    front_dist = measure_distance(Trig_back ,Echo_back )
    total      = right_dist + left_dist

    if   state == 0:
        if (front_dist < 12 and total > 25):
            obstacle(right_dist, left_dist)
            #state = 1
        else:
            bang_bang(right_dist, left_dist, total)

    elif state == 1:
        ret, frame = cap.read()
        angle = find_angle(frame)
        if abs(angle) < 3:
            motor_adj(0, 0, 1, 1)
            time.sleep(5)
            state = 0
        elif (front_dist < 12 and total > 25):
            obstacle(right_dist,left_dist)
            state = 2
            print 'state 1'
        else:
            bang_bang(right_dist, left_dist, total)

    elif state == 2:
        if front_dist < dist_1:
            motor_adj(0, 0, 1, 1)
            time.sleep(5)
            state = 3
            print 'state 2'
        else:
            bang_bang(right_dist, left_dist, total)

    elif state == 3:
        if (front_dist < 12 and total > 25):
            obstacle(right_dist, left_dist)
            state = 4
            print 'state 3'
        else:
            bang_bang(right_dist, left_dist, total)

    elif state == 4:
        if back_dist > dist_2:
            motor_adj(0, 0, 1, 1)
            time.sleep(5)
            state = 5
            print 'state 4'
        else:
            bang_bang(right_dist, left_dist, total)

    elif state == 5:
        if (back_dist < 12 and total > 25): # buraya bakma
            obstacle_inv(right_dist, left_dist)
            state = 6
            print 'state 5'
        else:
            bang_bang_inv(right_dist, left_dist, total)

    elif state == 6:
        if back_dist < dist_3:
            motor_adj(0, 0, 1, 1)
            time.sleep(5)
            state = 0
            print 'state 6'
        else:
            bang_bang_inv(right_dist, left_dist, total)

    elif state == 7:
        ret, frame = cap.read()
        angle = find_angle( frame )
        if abs(angle) < 3:
            motor_adj(0, 0, 1, 1)
            time.sleep(5)
            state = 0
        else:
            bang_bang(right_dist,left_dist,total)
