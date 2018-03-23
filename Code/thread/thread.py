import os
import threading
import cv2
import datetime,time
from angle_new_trial import Angle
from  turn_new_trial import Turn
from  mode_new_trial import Mode

def cam1(): #camera for angle measurement
    while(True):
        Plank.measurement(cam_1)
        Plank.value()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam_1.release()
    cv2.destroyWindow("Find_angle")

def cam2(): #camera for maze turn type
    while(True):
	Type.check(cam_2,-1)
        if cv2.waitKey(1) & 0xFF == ord('r'):
            break
    cam_2.release()
    cv2.destroyWindow('Walls')

def mode(): #master-slave
    while True:
        Mode_of_the_robot.check()
        print Mode_of_the_robot.is_slave()
    pass

Mode_of_the_robot = Mode()

os.system("sudo ln -s /dev/v4l/by-path/pci-0000\:00\:14.0-usb-0\:11* /dev/cam1 ")#symlink
os.system("sudo ln -s /dev/v4l/by-path/pci-0000\:00\:14.0-usb-0\:12* /dev/cam2 ")#symlink

Plank = Angle()
cam_1 = cv2.VideoCapture("/dev/cam1")
while True:
    print "Cam1 is being adjusted"
    if (cam_1.isOpened()) :  # check if we succeeded
        cam_1.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        cam_1.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
	break

Type=Turn()
cam_2 = cv2.VideoCapture("/dev/cam2")
while True:
    print "Cam2 is being adjusted"
    if (cam_2.isOpened()) :  # check if we succeeded
        cam_2.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        cam_2.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
	break


t1 = threading.Thread(target=cam1,name='cam1')
t2 = threading.Thread(target=cam2,name='cam2')
t3 = threading.Thread(target=mode,name='mode')
t1.start()
t2.start()
t3.start()
