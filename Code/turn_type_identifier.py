import cv2
import numpy as np
from math import atan2,degrees,sqrt
from numpy import zeros, newaxis
########################################################################

def vertical_lines(img):

    negative=negative_image(img)

    gray_image = cv2.cvtColor(negative, cv2.COLOR_BGR2GRAY)

    mask_white = cv2.inRange(gray_image, 200, 255)

    mask_w_image = cv2.bitwise_and(gray_image, mask_white)

    kernel_size = (5,5)
    gauss_gray = cv2.GaussianBlur(mask_w_image,kernel_size, 0)

    low_threshold = 50
    high_threshold = 150
    canny_edges = cv2.Canny(gauss_gray,low_threshold,high_threshold)

    #roi_image = select_region(canny_edges)

    list_of_lines = hough_lines(canny_edges)


 
    list_of_lines_vertical = eliminate_horizontal(list_of_lines)



    distin_list_of_lines_vertical = eliminate_similar_lines(list_of_lines_vertical)
    cv2.imshow('Original',img)
    cv2.imshow('Negative',negative)
    cv2.imshow('Gray',gray_image)
    cv2.imshow('mask_white',mask_white)
    cv2.imshow('mask_w_image',mask_w_image)
    cv2.imshow('gauss_gray',gauss_gray)
    cv2.imshow('canny_edges',canny_edges)
    cv2.waitKey(0)
    return distin_list_of_lines_vertical

def rotate_90(img):
    (h, w) = img2.shape[:2]
    center = (w / 2, h / 2)
 
    # rotate the image by 90 degrees
    M = cv2.getRotationMatrix2D(center, 90, 1.0)
    rotated = cv2.warpAffine(img2, M, (w, h))
    return rotated


def negative_image(img):
	return 255-img

def image_square_maker(img):
    height, width = img.shape[:2]
    a = [height,width]
    min_len = min(a)
    img = img[0:min_len,0:min_len]
    return img


def array_subs_3d(arr1,arr2):
    length = len ( arr1 )
    i = length - 1
    while True:
	for element in arr2:
	    [a,b,c,d] = np.ravel(element)
	    [e,f,g,h] = np.ravel(arr1[i])
            if ((a == e) & (b == f) & (c == g) & (d == h) ):
	        arr1 = np.delete(arr1,i,0)
		break
	i = i - 1
	if i == -1:
	    break
    return arr1
    

def filter_region(image, vertices):
    """
    Create the mask using the vertices and apply it to the input image
    """
    mask = np.zeros_like(image)
    if len(mask.shape)==2:
        cv2.fillPoly(mask, vertices, 255)
    else:
        cv2.fillPoly(mask, vertices, (255,)*mask.shape[2]) # in case, the input image has a channel dimension
    return cv2.bitwise_and(image, mask)


def select_region(image):
    """
    It keeps the region surrounded by the `vertices` (i.e. polygon).  Other area is set to 0 (black).
    """
    # first, define the polygon by vertices
    rows, cols = image.shape[:2]
    bottom_left  = [cols*0.1, rows*0.95]
    top_left     = [cols*0.4, rows*0.6]
    bottom_right = [cols*0.9, rows*0.95]
    top_right    = [cols*0.6, rows*0.6]
    # the vertices are an array of polygons (i.e array of arrays) and the data type must be integer
    vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    return filter_region(image, vertices)

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



####################################
def average_slope_intercept(lines):
    left_lines    = [] # (slope, intercept)
    left_weights  = [] # (length,)
    right_lines   = [] # (slope, intercept)
    right_weights = [] # (length,)

    for line in lines:
        for x1, y1, x2, y2 in line:
            if x2==x1:
                continue # ignore a vertical line
            slope = (y2-y1)/(x2-x1)
            intercept = y1 - slope*x1
            length = np.sqrt((y2-y1)**2+(x2-x1)**2)
            if slope < 0: # y is reversed in image
                left_lines.append((slope, intercept))
                left_weights.append((length))
            else:
                right_lines.append((slope, intercept))
                right_weights.append((length))

    # add more weight to longer lines
    left_lane  = np.dot(left_weights,  left_lines) /np.sum(left_weights)  if len(left_weights) >0 else None
    right_lane = np.dot(right_weights, right_lines)/np.sum(right_weights) if len(right_weights)>0 else None

    return left_lane, right_lane # (slope, intercept), (slope, intercept)


def make_line_points(y1, y2, line):
    """
    Convert a line represented in slope and intercept into pixel points
    """
    if line is None:
        return None

    slope, intercept = line

    # make sure everything is integer as cv2.line requires it
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    y1 = int(y1)
    y2 = int(y2)

    return ((x1, y1), (x2, y2))


def lane_lines(image, lines):
    left_lane, right_lane = average_slope_intercept(lines)

    y1 = image.shape[0] # bottom of the image
    y2 = y1*0.6         # slightly lower than the middle

    left_line  = make_line_points(y1, y2, left_lane)
    right_line = make_line_points(y1, y2, right_lane)

    return left_line, right_line


def draw_lane_lines(image, lines, color=[255, 0, 0], thickness=20):
    # make a separate image to draw lines and combine with the orignal later
    line_image = np.zeros_like(image)
    for line in lines:
        if line is not None:
            cv2.line(line_image, line,  color, thickness)
    # image1 * alfa + image2 * beta + lambda
    # image1 and image2 must be the same shape.
    return cv2.addWeighted(image, 1.0, line_image, 0.95, 0.0)
####################################

########################################################################

image = image_square_maker(cv2.imread('30.jpg'))
img = image_square_maker(cv2.imread('30.jpg'))
img2 = image_square_maker(cv2.imread('30.jpg'))
img3 = image_square_maker(cv2.imread('30.jpg'))



height, width = img2.shape[:2]
img2 = rotate_90(image)
top_horizontal_line=vertical_lines(img2)
x=[]
for line in top_horizontal_line:
    [x1, y1, x2, y2]=np.ravel(line)
    x.append(x1)
a = min([(v,i) for i,v in enumerate(x)])
min_line_index = a[1]
top_horizontal_line = top_horizontal_line [min_line_index]
[x1, y1, x2, y2]=np.ravel(top_horizontal_line)
top_horizontal_line = np.array([[height-y1, x1, height-y2, x2]])
top_horizontal_line = top_horizontal_line[newaxis , : , :]
vertical = vertical_lines(image)
all_lines = np.append(vertical , top_horizontal_line,axis=0)



fixed_vertical = vertical[0]
fixed_vertical = fixed_vertical[newaxis, :,:]
for line in vertical:
    [x1, y1, x2, y2]=np.ravel(line)
    xDiff = x2 - x1
    yDiff = y2 - y1
    slope = degrees(atan2(yDiff, xDiff))
    if slope > 0:
	line_fixed = np.array([[[max(x1,x2),y1,max(x1,x2),y2]]])
    else:
	line_fixed = np.array([[[min(x1,x2),y1,min(x1,x2),y2]]])
    fixed_vertical = np.append(fixed_vertical , line_fixed, axis=0)
fixed_vertical = np.delete(fixed_vertical , 0,0)



img = draw_lines_g(img , all_lines)
img = draw_lines_r(img , fixed_vertical)
legend = cv2.imread('legend.jpg' , cv2.IMREAD_COLOR)
img[0:45,0:231]  = legend[0:45,0:231]
#fixed_all = np.append(fixed_vertical , top_horizontal_line, axis=0)






x=[]
for line in fixed_vertical:
    [x1, y1, x2, y2]=np.ravel(line)
    x.append(x1)



def nearest_array_element(arr,near_2):
    arr = np.array(arr)
    idx = (np.abs(arr - near_2 )).argmin()
    return idx

x1, x2, x3, x4=-1, -1, -1, -1
i1 = nearest_array_element(x , height / 2)
x1 = x.pop(i1)
i2 = nearest_array_element(x , height / 2)
x2 = x.pop(i2)


if len(x) != 0 : 
    i3 = nearest_array_element(x , height / 2)
    x3 = x.pop(i3)
if len(x) != 0 : 
    i4 = nearest_array_element(x , height / 2)
    x4 = x.pop(i4)
dist = abs(x1 - x2)
dist = dist * 1.5



left = 0
right = 0

if ( (x3 != -1) and ( abs(x3 - x1) < dist or abs(x3 - x2) < dist ) ):    
    if x3 - (height / 2 ) < 0 :
	left = 1
    else :
	right = 1
if ( (x4 != -1) and ( abs(x4 - x1) < dist or abs(x4 - x2) < dist ) ):    
    if x3 - (height / 2 ) < 0 :
	left = 1
    else :
	right = 1 
else:
     if left == 0:
	left = -1
     if right == 0:
    	right = -1
if right == 1:
    print "Right -> U-Turn \n"
else:
    print "Right -> L-Turn \n"
if left == 1:
    print "Left -> U-Turn \n"
else:
    print "Left -> L-Turn \n"



#cv2.imshow('roi_image',roi_image)
cv2.imshow('Result',img)
#cv2.imshow('Result2',img33)
#cv2.imshow('Result3',img11)
cv2.waitKey(0)
cv2.destroyAllWindows()
