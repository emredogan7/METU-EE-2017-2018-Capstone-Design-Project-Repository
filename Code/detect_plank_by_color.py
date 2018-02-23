import cv2
import numpy as np
 
img = cv2.imread('circles.png', 1)

#convert to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


lower_range = np.array([169, 100, 100], dtype=np.uint8)
upper_range = np.array([189, 255, 255], dtype=np.uint8)

mask = cv2.inRange(hsv, lower_range, upper_range)
 
cv2.imshow('mask',mask)
cv2.imshow('image', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
