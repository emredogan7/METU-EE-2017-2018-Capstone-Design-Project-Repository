# import the necessary packages
import imutils
import cv2
from operator import add
from operator import div
import numpy as np
from math import atan2,degrees,sqrt


##########################################################################
#detect_plank_by_color

img = cv2.imread('input.jpg', 1)


#convert to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


lower_range = np.array([169, 100, 100], dtype=np.uint8)
upper_range = np.array([189, 255, 255], dtype=np.uint8)

mask = cv2.inRange(hsv, lower_range, upper_range)

cv2.imshow('Original', img)
cv2.imshow('Masked', mask)
cv2.imwrite('Masked.png',mask)
cv2.waitKey(0)

##########################################################################
#shape_fixer

# load the image, convert it to grayscale, and blur it slightly
fixed = cv2.imread("Masked.png")
gray = cv2.cvtColor(fixed, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# threshold the image, then perform a series of erosions +
# dilations to remove any small regions of noise
thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)

# find contours in thresholded image, then grab the largest
# one
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
c = max(cnts, key=cv2.contourArea)


# draw the outline of the object, then draw each of the
# extreme points, where the left-most is red, right-most
# is green, top-most is blue, and bottom-most is teal
cv2.drawContours(fixed, [c], -1, (255, 255, 255), -1)

# show the output image
cv2.imshow("Fixed", fixed)
cv2.imwrite('Fixed.png',fixed)
cv2.waitKey(0)


##########################################################################
#rectangle_transform

# read and scale down image
transformed = cv2.imread("Fixed.png")

# threshold image
ret, threshed_img = cv2.threshold(cv2.cvtColor(transformed, cv2.COLOR_BGR2GRAY),
                127, 255, cv2.THRESH_BINARY)
# find contours and get the external one
image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(transformed,[box],0,(255,255,255),-1)

cv2.imshow("Transformed", transformed)
cv2.imwrite('Transformed.png',transformed)
cv2.waitKey(0)


##########################################################################
#angle_of_planck


def angle(p1, p2):
        xDiff = p2[0] - p1[0]
        yDiff = p2[1] - p1[1]
        yDiff = yDiff * ( - 1 )
        return degrees(atan2(yDiff, xDiff)) - 90

def dist(tp1,tp2):
	x=tp1[0]-tp2[0]
	y=tp1[1]-tp2[1]
	return 	sqrt(x ** 2 + y ** 2)


# read and scale down image
find_angle = cv2.imread("Transformed.png")

# threshold image
ret, threshed_img = cv2.threshold(cv2.cvtColor(find_angle, cv2.COLOR_BGR2GRAY),
                127, 255, cv2.THRESH_BINARY)
# find contours and get the external one
image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE)

# with each contour, draw boundingRect in green
# a minAreaRect in red and
# a minEnclosingCircle in blue

tp1=()
tp2=()
tp3=()
tp4=()



for c in contours:


####################

    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(find_angle,[box],0,(0,0,255),2)

    tp1=tp1+tuple((box[2]+box[3])/2)
    tp2=tp2+tuple((box[0]+box[1])/2)

    tp3=tp3+tuple((box[1]+box[2])/2)
    tp4=tp4+tuple((box[0]+box[3])/2)

    if dist(tp1,tp2) > dist(tp3,tp4):
    	img = cv2.line(find_angle,tp2,tp1,(124,252,0),5)
    else:	
	img = cv2.line(find_angle,tp4,tp3,(124,252,0),5)
	tp1=tp4
	tp2=tp3
        #tp3-tp4 may be wrong check the angles and change if not true

####################
f = open('angle.txt','w')
value = 0 
if np.asarray(tp2)[1] > np.asarray(tp1)[1] :
    value = (angle(np.asarray(tp2),np.asarray(tp1)))
    print "Angle :" , angle(np.asarray(tp2),np.asarray(tp1))
else :
    value = (angle(np.asarray(tp1),np.asarray(tp2)))
    print "Angle :" , angle(np.asarray(tp1),np.asarray(tp2))

s = str(value)
f.write(s)
f.closed

cv2.drawContours(find_angle, contours, -1, (255, 255, 0), 1)
cv2.imshow("Find_angle", find_angle)
cv2.imwrite("Find_angle.png", find_angle)

cv2.waitKey(0)
cv2.destroyAllWindows()
















