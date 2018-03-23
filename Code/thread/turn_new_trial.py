# -*- coding: utf-8 -*-
import imutils
import cv2
from operator import add
from operator import div
import numpy as np
from math import atan2,degrees,sqrt
import os
import datetime,time
from numpy import zeros, newaxis

class Turn:
    'Description of the code'
    RIGHT = 0
    LEFT = 0

    def __init__(self) :
        print "Camera is being adjusting! \n"
 

    def vertical_lines(self,img):

        negative=self.negative_image(img)

        gray_image = cv2.cvtColor(negative, cv2.COLOR_BGR2GRAY)

        mask_white = cv2.inRange(gray_image, 200, 255)

        mask_w_image = cv2.bitwise_and(gray_image, mask_white)

        kernel_size = (5,5)
        gauss_gray = cv2.GaussianBlur(mask_w_image,kernel_size, 0)

        low_threshold = 50
        high_threshold = 150
        canny_edges = cv2.Canny(gauss_gray,low_threshold,high_threshold)



        list_of_lines = self.hough_lines(canny_edges)



        list_of_lines_vertical = self.eliminate_horizontal(list_of_lines)



        distin_list_of_lines_vertical = self.eliminate_similar_lines(list_of_lines_vertical)

        return distin_list_of_lines_vertical

    def rotate_90(self,img):
        (h, w) = img.shape[:2]
        center = (w / 2, h / 2)

        # rotate the image by 90 degrees
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h))
        return rotated


    def negative_image(self,img):
    	return 255-img

    def image_square_maker(self,img):
        height, width = img.shape[:2]
        a = [height,width]
        min_len = min(a)
        img = img[0:min_len,0:min_len]
        return img


    def filter_region(self,image, vertices):
        """
        Create the mask using the vertices and apply it to the input image
        """
        mask = np.zeros_like(image)
        if len(mask.shape)==2:
            cv2.fillPoly(mask, vertices, 255)
        else:
            cv2.fillPoly(mask, vertices, (255,)*mask.shape[2]) # in case, the input image has a channel dimension
        return cv2.bitwise_and(image, mask)


    def select_region(self,image):
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
        return self.filter_region(image, vertices)

    def hough_lines(self,image):
        """
        `image` should be the output of a Canny transform.
        Returns hough lines (not the image with lines)
        """
        return cv2.HoughLinesP(image, rho=1, theta=np.pi/180, threshold=20, minLineLength=20, maxLineGap=300)

    def draw_lines_g(self,image, lines, color=[0, 255, 0], thickness=2, make_copy=True):
        # the lines returned by cv2.HoughLinesP has the shape (-1, 1, 4)
        if make_copy:
            image = np.copy(image) # don't want to modify the original
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(image, (x1, y1), (x2, y2), color, thickness)
        return image

    def draw_lines_b(self,image, lines, color=[255, 0, 0], thickness=2, make_copy=True):
        # the lines returned by cv2.HoughLinesP has the shape (-1, 1, 4)
        if make_copy:
            image = np.copy(image) # don't want to modify the original
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(image, (x1, y1), (x2, y2), color, thickness)
        return image

    def draw_lines_r(self,image, lines, color=[0, 0, 255], thickness=2, make_copy=True):
        # the lines returned by cv2.HoughLinesP has the shape (-1, 1, 4)
        if make_copy:
            image = np.copy(image) # don't want to modify the original
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(image, (x1, y1), (x2, y2), color, thickness)
        return image

    def eliminate_horizontal(self,lines):
        ver_lin=[]
        if (lines is None) or (not lines.size):
            return
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


    def eliminate_similar_lines(self,lines):
        if (lines is None) or (not lines.size):
            return
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

    def nearest_array_element(self,arr,near_2):
        print ""
        arr = np.array(arr)
        idx = (np.abs(arr - near_2 )).argmin()
        return idx

    def __type_identifier(self,frame):
        image = self.image_square_maker(imutils.resize(frame,width=160))
        img = image
        img2 = image




        height, width = img2.shape[:2]
        img2 = self.rotate_90(image)
        top_horizontal_line=self.vertical_lines(img2)
        x=[]
        if (top_horizontal_line is None) or (not top_horizontal_line.size):
            Turn.RIGHT = -99
            Turn.LEFT = -99
            return
        for line in top_horizontal_line:
            [x1, y1, x2, y2]=np.ravel(line)
            x.append(x1)
        a = min([(v,i) for i,v in enumerate(x)])
        min_line_index = a[1]
        top_horizontal_line = top_horizontal_line [min_line_index]
        [x1, y1, x2, y2]=np.ravel(top_horizontal_line)
        top_horizontal_line = np.array([[height-y1, x1, height-y2, x2]])
        top_horizontal_line = top_horizontal_line[newaxis , : , :]
        vertical = self.vertical_lines(image)
        if (vertical is None) or (not vertical.size):
            Turn.RIGHT = -99
            Turn.LEFT = -99
            return
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



        img = self.draw_lines_g(img , all_lines)
        img = self.draw_lines_r(img , fixed_vertical)






        x=[]
        for line in fixed_vertical:
            [x1, y1, x2, y2]=np.ravel(line)
            x.append(x1)




        x1, x2, x3, x4=-1, -1, -1, -1
        left = -99
        right = -99

        if len(x) != 0 :
            i1 = self.nearest_array_element(x , height / 2)
            x1 = x.pop(i1)

            if len(x) != 0 :
                i2 = self.nearest_array_element(x , height / 2)
                x2 = x.pop(i2)
                left = 0
                right = 0

                if len(x) != 0 :
                    i3 = self.nearest_array_element(x , height / 2)
                    x3 = x.pop(i3)
                if len(x) != 0 :
                    i4 = self.nearest_array_element(x , height / 2)
                    x4 = x.pop(i4)
                dist = abs(x1 - x2)
                dist = dist * 1.5

                if ( (x3 != -1) and ( abs(x3 - x1) < dist or abs(x3 - x2) < dist ) ):
                    if x3 - (height / 2 ) < 0 :
                	    left = 1
                    else :
                	    right = 1
                if ( (x4 != -1) and ( abs(x4 - x1) < dist or abs(x4 - x2) < dist ) ):
                    if x4 - (height / 2 ) < 0 :
                	    left = 1
                    else :
                	    right = 1
                elif (x3 != -1):
                     if left == 0:
                	     left = -1
                     if right == 0:
                    	 right = -1

        Turn.RIGHT = right
        Turn.LEFT = left

        img = imutils.resize(img,width=640)
        cv2.imshow('Walls',img)

    def check(self,cap,direction):#-1 for right
        ret, frame = cap.read()
        self.__type_identifier(frame)
        if direction == -1:
            if Turn.RIGHT == 1:
                print "Right -> U-Turn \n"
            elif Turn.RIGHT == -1:
                print "Right -> L-Turn \n"
            elif Turn.RIGHT == 0:
                print "No Turns \n"
            else:
                print "Error line 316 (Two wall is not detected) "
        else:
            if Turn.LEFT == 1:
                print "Left -> U-Turn \n"
            elif Turn.LEFT == -1:
                print "Left -> L-Turn \n"
            elif Turn.LEFT == 0:
                print "No Turns \n"
            else:
                print "Error line 323 (Two wall is not detected)"
