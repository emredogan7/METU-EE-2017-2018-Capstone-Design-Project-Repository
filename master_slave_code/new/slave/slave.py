from sensor import set_distance_hw
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
set_distance_hw(Trig_left ,Echo_left)
set_distance_hw(Trig_back ,Echo_back)


"""
state 2 -> front distance = 45.0
state 4 -> front distance = 27.0
state 6 -> back distance = 32.5
"""

state  = 0
dist_1 = 4
dist_2 = 27
empty_side = 0

def get_wall(cap):#eksik
    ret, frame = cap.read()
    angle = find_angle(frame)
    return angle

def wait():
    motor_adj(0, 0, 1, 1)
    time.sleep(5)

while True:
    cap = cv2.VideoCapture(0)
    print "Angle_cam is being adjusted"
    if (cap.isOpened()) :  #check if we succeeded
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        break

while True:

if   state == 0:
    ret, img = cap.read()
    empty_side = wall_state_zero(img)
    if ( empty_side != 0 ):
        if is_L(img,empty_side):
            state = 'L_0'
        else:
            state = 'U_0'
    else:
        bang_bang()
elif state == 'L_0' or 'U_0':
    ret, img = cap.read()
    pos = wall_state_one(img,empty_side)
    if pos > 60 :
        wait()
        if state == 'L_0':
            state = 'L_1'
        else:
            state = 'U_1'
    else:
        bang_bang()
elif state == 'L_1':
    if (front_dist < 12 and total > 25):
        obstacle(right_dist, left_dist)
        state = 0
    else:
        bang_bang(right_dist, left_dist, total)
elif state == 'U_1':
    if back_dist < dist_1:
        wait()
        state = 2
    else:
        bang_bang_inv(right_dist, left_dist, total)
elif state == 2:
    if (back_dist < 12 and total > 25):
        obstacle_inv(right_dist, left_dist)
        state = 3
    else:
        bang_bang_inv(right_dist, left_dist, total)
elif state == 3:
    if back_dist > dist_2:
        wait()
        state = 4
    else:
        bang_bang(right_dist, left_dist, total)
elif state == 4:
    if ( back_dist < 12 and total > 25 ):
        obstacle_inv(right_dist, left_dist)
        state = 5
    else:
        bang_bang_inv(right_dist, left_dist, total)
elif state == 5:
    if back_dist > dist_2:
        wait()
        state = 6
    else:
        bang_bang(right_dist, left_dist, total)
elif state == 6:
    if (back_dist < 12 and total > 25):
        obstacle_inv(right_dist, left_dist)
        state = 7
    else:
        bang_bang_inv(right_dist, left_dist,total)
elif state == 7:
    if (back_dist < 12 and total > 25):
        obstacle_inv(right_dist, left_dist)
        state = 0
    else:
        bang_bang_inv(right_dist, left_dist, total)
