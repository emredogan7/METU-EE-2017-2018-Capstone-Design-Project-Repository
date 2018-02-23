import cv2
import numpy as np
from math import atan2,degrees



def angle(p1, p2):
        xDiff = p2[0] - p1[0]
        yDiff = p2[1] - p1[1]
        yDiff = yDiff * ( - 1 )
        return degrees(atan2(yDiff, xDiff)) - 90


# read and scale down image
img = cv2.imread("recta.jpg")

# threshold image
ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                127, 255, cv2.THRESH_BINARY)
# find contours and get the external one
image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE)

# with each contour, draw boundingRect in green
# a minAreaRect in red and
# a minEnclosingCircle in blue

tp1=()
tp2=()

for c in contours:


####################

    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img,[box],0,(0,0,255),2)


    tp1=tp1+tuple((box[2]+box[3])/2)
    tp2=tp2+tuple((box[0]+box[1])/2)
    img = cv2.line(img,tp2,tp1,(255,0,0),5)

####################

if np.asarray(tp2)[1] > np.asarray(tp1)[1] :
    print "Angle :" , angle(np.asarray(tp2),np.asarray(tp1))
else :
    print angle(np.asarray(tp1),np.asarray(tp2))


cv2.drawContours(img, contours, -1, (255, 255, 0), 1)

cv2.imshow("contours", img)


cv2.waitKey(0)
cv2.destroyAllWindows()
