# -*- coding: utf-8 -*-
import imutils
import cv2
from operator import add
from operator import div
import numpy as np
from math import atan2,degrees,sqrt
import os
import datetime,time

class Angle:
    'Description of the code'
    Value = -9999999

    def __init__(self) :
        print "Camera is being adjusting! \n"
        empty = []
        b = []
        while True:
            os.system("ls -la /dev/video* > camera.txt")
            filename = "camera.txt"
            file = open(filename, "r")
            a = file.read()
            b = list(a)
            if b == empty:
        	    print "Camera is not detected! \n"
        	    file.close()
        	    continue
            string_2 = str(b[-2])
            file.close()
            print "Camera is detected! \n"
            break

        string_1 = "mv /dev/video"
        string_3 = " /dev/video0"

        complete = string_1 + string_2 + string_3

        os.system("sudo chmod -R 777 /dev")
        os.system(complete)

        while(True):
            cap = cv2.VideoCapture(0)

            if (cap.isOpened()):
        	cap.set(cv2.CAP_PROP_FRAME_WIDTH,640);
        	cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480);
                break

            print "\nCould not access camera! \n"


    def value(self) :
        if Angle.Value == -9999999 :
            print "Plank is not detected! \n"
        else :
            print "Angle : ",Angle.Value
            return Angle.Value




    def measurement(self,cap) :

        ret, frame = cap.read()
        Angle.Value = self.__measurement_angle(frame)

    def __measurement_angle(self, frame): #private function

        img = imutils.resize(frame,width=160)

#detect_plank_by_color

    	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    	lower_range = np.array([0, 100, 100], dtype=np.uint8)
    	upper_range = np.array([10, 255, 255], dtype=np.uint8)
    	mask_1 = cv2.inRange(hsv, lower_range, upper_range)
    	lower_range = np.array([170, 100, 100], dtype=np.uint8)
    	upper_range = np.array([180, 255, 255], dtype=np.uint8)
    	mask_2 = cv2.inRange(hsv, lower_range, upper_range)
    	mask = cv2.bitwise_or(mask_1, mask_2)

#shape_fixer

    	gray = mask
    	gray = cv2.GaussianBlur(gray, (5, 5), 0)
    	thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    	thresh = cv2.erode(thresh, None, iterations=2)
    	thresh = cv2.dilate(thresh, None, iterations=2)
    	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

#angle_of_planck

    	if cnts :
    		c = max(cnts, key=cv2.contourArea)
    		cv2.drawContours(mask, [c], -1, (255, 255, 255), -1)


    		def angle(p1, p2):
    			xDiff = p2[0] - p1[0]
    			yDiff = p2[1] - p1[1]
    			yDiff = yDiff * ( - 1 )
    			return degrees(atan2(yDiff, xDiff)) - 90
    		def dist(tp1,tp2):
    			x=tp1[0]-tp2[0]
    			y=tp1[1]-tp2[1]
    			return 	sqrt(x ** 2 + y ** 2)

    		image, contours, hier = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    		tp1=()
    		tp2=()
    		tp3=()
    		tp4=()

    		textX = 0
    		textY = 0

    		con_area = []
    		for c in contours:
        		con_area.append(cv2.contourArea(c))

    		max_area_index = con_area.index(max(con_area))

    		rect = cv2.minAreaRect(contours[max_area_index])
    		box = cv2.boxPoints(rect)
    		box = np.int0(box)
    		cv2.drawContours(mask,[box],0,(0,0,255),2)

    		tp1=tp1+tuple((box[2]+box[3])/2)
    		tp2=tp2+tuple((box[0]+box[1])/2)

    		tp3=tp3+tuple((box[1]+box[2])/2)
    		tp4=tp4+tuple((box[0]+box[3])/2)

    		height, width = mask[:2]

    		if dist(tp1,tp2) > dist(tp3,tp4):
    			if tp1[0] == tp2[0] :
    			    x = [tp1[1], tp2[1]]
    			    y = [tp1, tp2]
    			    max_index = x.index(max(x))
    			    min_index = 1 - max_index
    			    img = cv2.arrowedLine(img,y[max_index],y[min_index],(124,252,0),5)
    			elif tp1[1] == tp2[1] :
    			    x = [tp1[0], tp2[0]]
    			    y = [tp1, tp2]
    			    max_index = x.index(max(x))
    			    min_index = 1 - max_index
    			    if  x[max_index] > ( width.size * 1.1 / 6 ) :
    			    	img = cv2.arrowedLine(img,y[min_index],y[max_index],(124,252,0),5)
    			    else :
    			    	img = cv2.arrowedLine(img,y[max_index],y[min_index],(124,252,0),5)
    			else :
    			    x = [tp1[0], tp2[0]]
    			    y = [tp1, tp2]
    			    max_index = x.index(max(x))
    			    min_index = 1 - max_index
    			    if y[max_index][1] < y[min_index][1]:
    			    	img = cv2.arrowedLine(img,y[min_index],y[max_index],(124,252,0),5)
    			    else :
    			    	img = cv2.arrowedLine(img,y[max_index],y[min_index],(124,252,0),5)
    			textX = ( tp1[0] + tp2[0] ) / 2 + 25
    			textY = ( tp1[1] + tp2[1] ) / 2 + 25
    		else:
    			tp1 = tp3
    			tp2 = tp4
    			if tp1[0] == tp2[0] :
    			    x = [tp1[1], tp2[1]]
    			    y = [tp1, tp2]
    			    max_index = x.index(max(x))
    			    min_index = 1 - max_index
    			    img = cv2.arrowedLine(img,y[max_index],y[min_index],(124,252,0),5)
    			elif tp1[1] == tp2[1] :
    			    x = [tp1[0], tp2[0]]
    			    y = [tp1, tp2]
    			    max_index = x.index(max(x))
    			    min_index = 1 - max_index
    			    if  x[max_index] > ( width.size * 1.1 / 6 )  :
    			    	img = cv2.arrowedLine(img,y[min_index],y[max_index],(124,252,0),5)
    			    else :
    			    	img = cv2.arrowedLine(img,y[max_index],y[min_index],(124,252,0),5)
    			else :
    			    x = [tp1[0], tp2[0]]
    			    y = [tp1, tp2]
    			    max_index = x.index(max(x))
    			    min_index = 1 - max_index
    			    if y[max_index][1] < y[min_index][1]:
    			    	img = cv2.arrowedLine(img,y[min_index],y[max_index],(124,252,0),5)
    			    else :
    			    	img = cv2.arrowedLine(img,y[max_index],y[min_index],(124,252,0),5)
    			textX = ( tp1[0] + tp2[0] ) / 2 + 25
    			textY = ( tp1[1] + tp2[1] ) / 2 - 25

    		value = 0
    		if np.asarray(tp2)[1] > np.asarray(tp1)[1] :
    			value = (angle(np.asarray(tp2),np.asarray(tp1)))
    		else :
    			value = (angle(np.asarray(tp1),np.asarray(tp2)))

    		x = [tp1[0], tp2[0]]
    		y = [tp1, tp2]
    		max_index = x.index(max(x))
    		min_index = 1 - max_index
    		if value == -90 and x[max_index] < ( width.size * 1.1 / 6 ) :
    			value = 90.0

    		value = int(value)
    		s = str(value)
    		font = cv2.FONT_HERSHEY_SIMPLEX
    		text = "Angle : " + s
    		textsize = cv2.getTextSize(text, font, 1, 2)[0]
    		cv2.putText(img, text, (textX, textY ), font, 1, (219, 255, 77), 2)



        img = imutils.resize(img,width=640)
    	cv2.imshow("Find_angle", img)


    	try:
    	    value # does a exist in the current namespace
    	except NameError:
    	    return -9999999
    	return value

Plank = Angle()
cap = cv2.VideoCapture(0)

















while(True):
    beginning = datetime.datetime.now().time().microsecond + datetime.datetime.now().time().second * 1000000
    Plank.measurement(cap)
    Plank.value()
    ending = datetime.datetime.now().time().microsecond + datetime.datetime.now().time().second * 1000000
    Fps = 1000000.0 / ( ending - beginning )
    print "Fps : ", Fps, "\n"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
