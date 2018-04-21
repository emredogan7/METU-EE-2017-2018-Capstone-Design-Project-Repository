import cv2
import numpy as np
from math import atan2,degrees,sqrt
from numpy import zeros, newaxis
########################################################################

def vertical_lines(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_range = np.array([0, 0, 0], dtype=np.uint8)
    upper_range = np.array([180, 255, 50], dtype=np.uint8)
    mask_1 = cv2.inRange(hsv, lower_range, upper_range)

    mask_2=cv2.bitwise_and(img,img,mask_1)


    negative=negative_image(mask_2)

    gray_image = cv2.cvtColor(negative, cv2.COLOR_BGR2GRAY)

    mask_white = cv2.inRange(gray_image, 200, 255)

    mask_w_image = cv2.bitwise_and(gray_image, mask_white)

    kernel_size = (5,5)
    gauss_gray = cv2.GaussianBlur(mask_w_image,kernel_size, 0)

    low_threshold = 50
    high_threshold = 150
    canny_edges = cv2.Canny(gauss_gray,low_threshold,high_threshold)



    list_of_lines = hough_lines(canny_edges)

    if list_of_lines is None:
        return

    list_of_lines_vertical = eliminate_horizontal(list_of_lines)



    distin_list_of_lines_vertical = eliminate_similar_lines(list_of_lines_vertical)
    #cv2.imshow('Original',img)
    #cv2.imshow('Negative',negative)
    #cv2.imshow('Gray',gray_image)
    #cv2.imshow('mask_white',mask_white)
    #cv2.imshow('mask_w_image',mask_w_image)
    #cv2.imshow('gauss_gray',gauss_gray)
    #cv2.imshow('canny_edges',canny_edges)
    #cv2.waitKey(0)
    return distin_list_of_lines_vertical

def rotate_90(img):
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)

    # rotate the image by 90 degrees
    M = cv2.getRotationMatrix2D(center, 90, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    return rotated


def negative_image(img):
	return 255-img

def image_square_maker(img):
    height, width = img.shape[:2]
    a = [height,width]
    min_len = min(a)
    img = img[0:min_len,0:min_len]
    return img


def hough_lines(image):
    """
    `image` should be the output of a Canny transform.
    Returns hough lines (not the image with lines)
    """
    return cv2.HoughLinesP(image, rho=1, theta=np.pi/180, threshold=20, minLineLength=20, maxLineGap=300)

def draw_lines_g(image, lines, color=[0, 255, 0], thickness=2, make_copy=True):
    # the lines returned by cv2.HoughLinesP has the shape (-1, 1, 4)
    if make_copy:
        image = np.copy(image) # don't want to modify the original
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), color, thickness)
    return image

def draw_lines_b(image, lines, color=[255, 0, 0], thickness=2, make_copy=True):
    # the lines returned by cv2.HoughLinesP has the shape (-1, 1, 4)
    if make_copy:
        image = np.copy(image) # don't want to modify the original
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), color, thickness)
    return image

def draw_lines_r(image, lines, color=[0, 0, 255], thickness=2, make_copy=True):
    # the lines returned by cv2.HoughLinesP has the shape (-1, 1, 4)
    if make_copy:
        image = np.copy(image) # don't want to modify the original
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), color, thickness)
    return image

def eliminate_horizontal(lines):
    ver_lin=[]
    for line in lines:
        [x1, y1, x2, y2]=np.ravel(line)
        xDiff = x2 - x1
        yDiff = y2 - y1
	if y1 == y2:
	    continue
	elif (abs(degrees(atan2(yDiff, xDiff)))) < 20:
	    continue
	else:
	    ver_lin.append(line)
    return np.array(ver_lin)


def eliminate_similar_lines(lines):
    new = lines[0]
    new = new[newaxis, :,:]
    i = 0
    for line in lines:
	[x1_lol, y1_lol, x2_lol, y2_lol]=np.ravel(line)
        for t in range( len(new) ):
	    [x1_l, y1_l, x2_l, y2_l]=np.ravel(new[t])
	    xDiff = x1_l - x1_lol
	    xDiff = abs(xDiff)
	    if xDiff < 50 :
		break
	    if len(new) - 1 == t :
		add = line
		add = add[newaxis, :, :,]
		new = np.append(new , add,axis=0)
    return new


########################################################################
def wall_position(ima):
    image = image_square_maker(ima)
    img = image
    img2 = image




    height, width = img2.shape[:2]
    img2 = rotate_90(image)
    horizontal_line=vertical_lines(img2)
    if horizontal_line is None:
        return

    x=[]
    for line in horizontal_line:
        [x1, y1, x2, y2]=np.ravel(line)
        x.append(x1)
    a = min([(v,i) for i,v in enumerate(x)])
    min_line_index = a[1]
    horizontal_line = horizontal_line [min_line_index]
    [x1, y1, x2, y2]=np.ravel(horizontal_line)
    horizontal_line = np.array([[height-y1, x1, height-y2, x2]])
    horizontal_line = horizontal_line[newaxis , : , :]

    return x1

    img = draw_lines_r(img , horizontal_line)



    cv2.imshow('Result',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    img = cv2.imread('1.jpg')
    print wall_position(img)
