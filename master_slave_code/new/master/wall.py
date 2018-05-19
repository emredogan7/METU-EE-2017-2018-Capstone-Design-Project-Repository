import numpy as np
import cv2,os
import math

def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def wall_state_zero(img):
    adjusted = adjust_gamma(img, gamma=0.5)
    right = adjusted[230:300,490:(490+75)]
    left  = adjusted[230:300,75:150]

    gray_left  = cv2.cvtColor(left,cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(right,cv2.COLOR_BGR2GRAY)

    ret,thresh_left  = cv2.threshold(gray_left,100,255,cv2.THRESH_BINARY)
    ret,thresh_right = cv2.threshold(gray_right,100,255,cv2.THRESH_BINARY)

    edges_left = cv2.Canny(thresh_left,50,100,apertureSize = 3)
    edges_right = cv2.Canny(thresh_right,50,100,apertureSize = 3)


    right_lines = []
    #print type(lines),lines.shape,lines[0],"ddddd"
    lines = cv2.HoughLines(edges_right,1,np.pi/180,20)
    if not lines is None:
        for i in  range(0,lines.shape[0]):
            rho,theta = lines[i,0]
            ang = ( theta / math.pi ) * 180
            if ang < 150 and ang > 140:
                right_lines.append((rho,theta))

    left_lines = []
    #print type(lines),lines.shape,lines[0],"ddddd"
    lines = cv2.HoughLines(edges_left,1,np.pi/180,20)
    if not lines is None:
        for i in  range(0,lines.shape[0]):
            rho,theta = lines[i,0]
            ang = ( theta / math.pi ) * 180
            if ang < 40 and ang > 30:
                left_lines.append((rho,theta))


    if not   len( right_lines ) :
        return -1
    elif not len( left_lines  ) :
        return  1
    else:
        return  0

def wall_state_one(img,left_or_right):
    adjusted = adjust_gamma(img, gamma=0.5)
    right = adjusted[120:300,490:]
    left  = adjusted[120:300,:150]

    gray_left  = cv2.cvtColor(left,cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(right,cv2.COLOR_BGR2GRAY)

    ret,thresh_left  = cv2.threshold(gray_left,100,255,cv2.THRESH_BINARY)
    ret,thresh_right = cv2.threshold(gray_right,100,255,cv2.THRESH_BINARY)

    edges_left = cv2.Canny(thresh_left,50,100,apertureSize = 3)
    edges_right = cv2.Canny(thresh_right,50,100,apertureSize = 3)


    right_lines = []
    #print type(lines),lines.shape,lines[0],"ddddd"
    lines = cv2.HoughLines(edges_right,1,np.pi/180,20)
    if not lines is None:
        for i in  range(0,lines.shape[0]):
            rho,theta = lines[i,0]
            ang = ( theta / math.pi ) * 180
            if ang < 92 and ang > 88:
                right_lines.append((rho,theta))

    left_lines = []
    #print type(lines),lines.shape,lines[0],"ddddd"
    lines = cv2.HoughLines(edges_left,1,np.pi/180,20)
    if not lines is None:
        for i in  range(0,lines.shape[0]):
            rho,theta = lines[i,0]
            ang = ( theta / math.pi ) * 180
            if ang < 92 and ang > 88:
                left_lines.append((rho,theta))

    if len( right_lines ) :
        rho   = max(right_lines)[0]
        theta = max(right_lines)[1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        y1 = int(y0 + 1000*(a))
        y2 = int(y0 - 1000*(a))
        center_right = ( y1 + y2 ) / 2
    else:
        center_right = -1

    if len( left_lines ) :
        rho   = max(left_lines)[0]
        theta = max(left_lines)[1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        y1 = int(y0 + 1000*(a))
        y2 = int(y0 - 1000*(a))
        center_left = ( y1 + y2 ) / 2
    else:
        center_left = -1

    if left_or_right == -1:
        return center_right
    else:
        return center_left

"""
cap = cv2.VideoCapture(0)
while True:
    print "Angle_cam is being adjusted"
    if ( cap.isOpened() ) :  # check if we succeeded
        cap.set( cv2.CAP_PROP_FRAME_WIDTH,  640 )
        cap.set( cv2.CAP_PROP_FRAME_HEIGHT, 480 )
        break
    cap = cv2.VideoCapture("/dev/cam1")

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()
    l_or_r =  wall_state_zero(img)
    print l_or_r
    print wall_state_one(img,l_or_r)
"""
