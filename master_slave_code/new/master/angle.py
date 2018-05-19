import imutils
import cv2
from operator import add
from operator import div
import numpy as np
from math import atan2,degrees,sqrt
import os

def detect_angle(  frame ): #private function

        img = imutils.resize( frame, width = 160 )

#detect_plank_by_color

    	hsv         = cv2.cvtColor( img, cv2.COLOR_BGR2HSV )
    	lower_range = np.array( [ 0, 100, 100 ], dtype = np.uint8 )
    	upper_range = np.array( [ 10, 255, 255 ], dtype = np.uint8 )
    	mask_1      = cv2.inRange( hsv, lower_range, upper_range )
    	lower_range = np.array( [ 170, 100, 100 ], dtype = np.uint8 )
    	upper_range = np.array( [ 180, 255, 255 ], dtype = np.uint8 )
    	mask_2      = cv2.inRange( hsv, lower_range, upper_range )
    	mask        = cv2.bitwise_or( mask_1, mask_2 )

#shape_fixer

    	gray   = mask
    	gray   = cv2.GaussianBlur( gray, ( 5, 5 ), 0 )
    	thresh = cv2.threshold( gray, 45, 255, cv2.THRESH_BINARY )[ 1 ]
    	thresh = cv2.erode( thresh, None, iterations = 2 )
    	thresh = cv2.dilate( thresh, None, iterations = 2 )
    	#cv2.imshow( "thresh", thresh )
    	cnts   = cv2.findContours( thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    	cnts   = cnts[ 0 ] if imutils.is_cv2() else cnts[ 1 ]

#angle_of_planck

    	if cnts :
    		c = max( cnts, key = cv2.contourArea )
    		cv2.drawContours( mask, [ c ], -1, ( 255, 255, 255 ), -1 )
    		cv2.drawContours( img, [ c ], -1, ( 0, 255, 255 ), 1 )
    		#print "asd",type(c),"dsa"

    		def angle( p1, p2 ):
    			xDiff = p2[ 0 ] - p1[ 0 ]
    			yDiff = p2[ 1 ] - p1[ 1 ]
    			yDiff = yDiff
    			return degrees( atan2( yDiff, xDiff ) )
    		def dist( tp1, tp2 ):
    			x=tp1[ 0 ]-tp2[ 0 ]
    			y=tp1[ 1 ]-tp2[ 1 ]
    			return 	sqrt( x ** 2 + y ** 2 )

    		image, contours, hier = cv2.findContours( mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )

    		tp1=()
    		tp2=()
    		tp3=()
    		tp4=()

    		con_area = []
    		for c in cnts:
        		con_area.append( cv2.contourArea( c ) )



    		max_area_index = con_area.index( max( con_area ) )
    		M = cv2.moments(cnts[max_area_index])
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
    		rect = cv2.minAreaRect( c )
    		box  = cv2.boxPoints( rect )
    		box  = np.int0( box)

    		middle = tuple((box[ 0 ] + box[ 1 ] + box[ 2 ] + box[ 3 ]) / 4)
		middle = (cX,middle[1])
    		if box[0][1] > middle[1]:
        		if box[1][1] > middle[1]:
				if box[0][0] < box[1][0]:
					lower_left  = tuple(box[0])
					lower_right = tuple(box[1])
				else:
					lower_right = tuple(box[0])
					lower_left  = tuple(box[1])
        		else:
				if box[0][0] < box[3][0]:
					lower_left  = tuple(box[0])
					lower_right = tuple(box[3])
				else:
					lower_right = tuple(box[0])
					lower_left  = tuple(box[3])
    		else:
        		if box[1][1] > middle[1]:
				if box[2][0] < box[1][0]:
					lower_left  = tuple(box[2])
					lower_right = tuple(box[1])
				else:
					lower_right = tuple(box[2])
					lower_left  = tuple(box[1])
        		else:
				if box[2][0] < box[3][0]:
					lower_left  = tuple(box[2])
					lower_right = tuple(box[3])
				else:
					lower_right = tuple(box[2])
					lower_left  = tuple(box[3])




    		bot = ((lower_left[0] + lower_right[0])/2,(lower_left[1] + lower_right[1])/2)
	        value = ( angle( np.asarray( middle ), np.asarray( bot ) ) )
	        img   = cv2.arrowedLine( img, bot, middle, ( 124, 252, 0 ), 5 )

    		value = 90 - value

    		if value == 180 :
    		    value = 0
    		elif value > 180 :
    		    value = value - 360

    		value    = int( value )
    		s        = str( value )
    		font     = cv2.FONT_HERSHEY_SIMPLEX
    		text     = "Ang:" + s
    		textsize = cv2.getTextSize( text, font, 1, 1 )[ 0 ]
    		textX    =  0
    		textY    =  25
    		cv2.putText( img, text, ( textX, textY ), font, 1, ( 219, 255, 77 ), 1 )



        #img = imutils.resize( img, width = 640 )
    	#cv2.imshow( "Find_angle", img )
	try:
		return value
	except NameError:
		return -99999

def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def cut(frame):
    height,width,temp = frame.shape
    mask = np.zeros((height,width,3), np.uint8)

    angle      = 20
    startAngle = 270 - angle
    endAngle   = 270 + angle
    r = 4000
    cv2.ellipse(mask, (width/2,(5*height/2)), (r,r), 0, startAngle, endAngle, (255,255,255), -1)

    mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
    ret, masked = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
    masked_data = cv2.bitwise_and(frame, frame, mask=masked)
    #cv2.imshow('asd',masked_data)
    return masked_data

def find_angle(frame):
    adjusted = adjust_gamma(frame, gamma=0.5)
    #cut = cut (adjusted)
    #cv2.imshow('Frame',cut (adjusted))
    angle      = 20
    startAngle = 270 - angle
    endAngle   = 270 + angle
    r = 4000
    height,width,temp = frame.shape
    ##cv2.imshow('asd',adjusted)
    cv2.ellipse(adjusted, (width/2,(5*height/2)), (r,r), 0, endAngle-1, (endAngle), (0,0,255), -1)
    cv2.ellipse(adjusted, (width/2,(5*height/2)), (r,r), 0, (startAngle), startAngle+2, (0,0,255), -1)
    cv2.ellipse(adjusted, (width/2,(height)), (480,480), 0, 180, 360, (255,0,0), 350)
    #cv2.imshow('asd',adjusted)

    angle = detect_angle(cut (adjusted))
    return angle

"""
cap = cv2.VideoCapture(0)
while True:
    print "Angle_cam is being adjusted"
    if ( cap.isOpened() ) :  # check if we succeeded
        cap.set( cv2.CAP_PROP_FRAME_WIDTH,  640 )
        cap.set( cv2.CAP_PROP_FRAME_HEIGHT, 480 )
        break
    cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    #cv2.imshow('asd',frame)
    angle = find_angle(frame)
    if abs (angle) < 3 :
        print "stop\n\n","<>"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
"""
