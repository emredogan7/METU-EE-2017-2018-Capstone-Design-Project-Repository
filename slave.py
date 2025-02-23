import os
import cv2
import

import imutils
import datetime,time

import numpy    as np
import RPi.GPIO as GPIO

from operator import div,div
from numpy    import zeros, newaxis
from math     import atan2,degrees,sqrt

from wall_position_slave import wall_position as m_w_p

mode = GPIO.getmode()
GPIO.setmode( GPIO.BCM )

class Slave():
    """This is the slave class that is a code combination
    to run our robot as the slave one which follows the master
    in the maze, collaboratively!"""



    Is_sys_stop  = False

    Stop_history = []
    Zero_history = []

    Angle        = -9999999
    Direction    = ''

    Angle_cam    = None
    Robot_cam    = None

    Trig_front   = 19
    Echo_front   = 26

    Trig_right   = 21
    Echo_right   = 20

    PWM_0        = None
    PWM_1        = None



    def __init__( self ):

        """---------------- GLOBAL_VARIABLE_INIT -----------------"""

        Slave.Stop_history.extend( [ 'Slave', 'Slave' ] )
        Slave.Zero_history.extend( [ 0, 0 ] )
        Slave.Direction    = 'Forward'

        """---------------- GLOBAL_VARIABLE_INIT - END -----------------"""

        """---------------- CAMERA_ADJUSTMENT -----------------"""

        os.system( "sudo ln -s /dev/v4l/by-path/platform-3f980000.usb-usb-0:1.4:1.0-video* /dev/cam1" )#symlink - modify that part right top hub
        os.system( "sudo ln -s /dev/v4l/by-path/platform-3f980000.usb-usb-0:1.5:1.0-video* /dev/cam2" )#symlink - modify that part right down hub

        Slave.Angle_cam    = cv2.VideoCapture( "/dev/cam1" )
        while True:
            print "Angle_cam is being adjusted"
            if ( Slave.Angle_cam.isOpened() ) :  # check if we succeeded
                Slave.Angle_cam.set( cv2.CAP_PROP_FRAME_WIDTH,  640 )
                Slave.Angle_cam.set( cv2.CAP_PROP_FRAME_HEIGHT, 480 )
                break

        Slave.Robot_cam    = cv2.VideoCapture( "/dev/cam2" )
        while True:
            print "Robot_cam is being adjusted"
            if ( Slave.Robot_cam.isOpened() ) :  # check if we succeeded
                Slave.Robot_cam.set( cv2.CAP_PROP_FRAME_WIDTH,  640 )
                Slave.Robot_cam.set( cv2.CAP_PROP_FRAME_HEIGHT, 480 )
                break

        """---------------- CAMERA_ADJUSTMENT - END -----------------"""

        """---------------- GPIO_ADJUSTMENT -----------------"""

        GPIO.setup( Slave.Trig_front, GPIO.OUT )
        GPIO.setup( Slave.Echo_front, GPIO.IN  )

        GPIO.setup( Slave.Trig_right, GPIO.OUT )
        GPIO.setup( Slave.Echo_right, GPIO.IN  )



        GPIO.setup(6 ,GPIO.OUT )
        GPIO.setup(5 ,GPIO.OUT )

        GPIO.setup(7 ,GPIO.OUT )
        GPIO.setup(8 ,GPIO.OUT )

        GPIO.setup(13,GPIO.OUT)
        GPIO.setup(12,GPIO.OUT)

        """---------------- GPIO_ADJUSTMENT - END -----------------"""

        """---------------- PWM_ADJUSTMENT -----------------"""


	Slave.PWM_0 = GPIO.PWM(13,100)
        Slave.PWM_1 = GPIO.PWM(12,100)

	Slave.PWM_0.start( 0 )
        Slave.PWM_1.start( 0 )

        """---------------- PWM_ADJUSTMENT - END -----------------"""

    """---------------- MEASURE_DISTANCE -----------------"""

    def measure_distance( self, TRIG, ECHO ):

        time.sleep( 0.1 )
        GPIO.output( TRIG, True )
        time.sleep( 0.00001)
        GPIO.output( TRIG, False )

        while GPIO.input( ECHO ) == 0:
            pulse_start = time.time()

        while GPIO.input( ECHO ) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round( distance, 2 )
        return distance

    """------------- MEASURE_DISTANCE - END --------------"""

    """---------------- FRONT_WALL_DIST -----------------"""

    def front_wall_dist( self ):
        return self.measure_distance( Slave.Trig_front, Slave.Echo_front )

    """------------- FRONT_WALL_DIST - END --------------"""

    """---------------- SIDE_WALL_DIST -----------------"""

    def side_wall_dist( self ):
        return self.measure_distance( Slave.Trig_right, Slave.Echo_right )

    """------------- SIDE_WALL_DIST - END --------------"""

    """---------------- MOTOR -----------------"""

    def motor( self, speed_right, speed_left, dir_right, dir_left ):


        dir_right_not = 1 - dir_right
        dir_left_not  = 1 - dir_left

        GPIO.output( 6, dir_right )
        GPIO.output( 5, dir_right_not )

        GPIO.output( 7, dir_left_not )
        GPIO.output( 8, dir_left )

        Slave.PWM_0.ChangeDutyCycle(speed_right)
        Slave.PWM_1.ChangeDutyCycle(speed_left)


    """------------- MOTOR - END --------------"""

    """---------------- WAIT -----------------"""

    def wait( self, time_to_wait ):
        self.motor( 0, 0, 0, 0 )
        time.sleep( time_to_wait )


    """------------- WAIT - END --------------"""

    """---------------- OBSTACLE -----------------"""

    def obstacle( self ):
        front_distance = self.front_wall_dist()
        if front_distance < 10:
            return True
        else:
            return False

    """------------- OBSTACLE - END --------------"""

    """---------------- TURN -----------------"""

    def turn( self, speed,time_for_process):
        right_distance = self.side_wall_dist()
        if right_distance < 25:
            self.motor( speed, 0, speed, 1 )
        else:
            self.motor( speed, 1, speed, 0 )
        time.sleep(time_for_process)

    """------------- TURN - END --------------"""

    """---------------- BANG_BANG -----------------"""

    def bang_bang( self, speed,time_for_process):
        right_distance = self.side_wall_dist()
        if right_distance <= 11:
            self.motor( speed + 10, 1, speed - 10, 1 )
            time.sleep(time_for_process)
        elif right_distance >= 13:
            self.motor( speed - 10, 1, speed + 10, 1 )
            time.sleep(time_for_process)
        else:
            self.motor( speed,      1, speed,      1 )
            time.sleep(time_for_process)


    """------------- BANG_BANG - END --------------"""

    """---------------- GO_STRAIGHT -----------------"""

    def go_straight( self, speed,time_for_process):
        self.motor( speed, 1, speed, 1 )
        time.sleep(time_for_process)
    """------------- GO_STRAIGHT - END --------------"""

    """---------------- STOP_HISTORY -----------------"""

    def history_check( self, arg ):
        return Slave.Stop_history[ arg ]

    def history_add_stop( self, stop_type ):
        Slave.Stop_history.append( stop_type )
        Slave.Stop_history.pop( 0 )

    """------------- STOP_HISTORY - END --------------"""

    """------------------ DIRECTION ------------------"""

    def positive_angle_change( self, diff):
        if diff > 0 :
            Slave.Direction = 'Backward'
        else:
            Slave.Direction = 'Forward'

    def negative_angle_change( self, diff):
        if diff > 0 :
            Slave.Direction = 'Forward'
        else:
            Slave.Direction = 'Backward'

    def detect_direction( self ):
        ret, frame_1 = Slave.Angle_cam.read()
        self.angle( frame_1 )
        Angle_1 = Slave.Angle

        Slave.wait(time_for_process) #az bekle

        ret, frame_2 = Slave.Angle_cam.read()
        self.angle( frame_2 )
        Angle_2 = Slave.Angle

        if ( Is_sys_stop ):
            Slave.Direction   = 'Forward'
            return

        elif ( Slave.Direction == 'Backward' ):
            Slave.Direction   = 'Forward'
            return

        else:
            if ( Angle_1 == 0 ):
                Slave.Direction   = 'Forward'
                return
            else:
                if ( Slave.Zero_history[ 1 ] == 'Master' ):
                    if ( Slave.Zero_history[ 0 ] == 'Slave' ):
                        positive_angle_change( abs( Angle_2 ) - abs( Angle_1 ) )
                    if ( Slave.Zero_history[ 0 ] == 'Master' ):
                        negative_angle_change( abs( Angle_2 ) - abs( Angle_1 ) )
                elif ( Slave.Zero_history[ 1 ] == 'Slave' or Slave.Zero_history[ 1 ] == 'Sys' ):
                    if ( abs( Angle ) > 90 ):
                        Slave.Direction   = 'Forward'
                        return
                    else:
                        if ( Slave.Zero_history[ 0 ] == 'Master' ):
                            Slave.Direction   = 'Forward'
                            return
                        else:
                            if   ( Slave.Zero_history[ 0 ] == 'Slave' and Slave.Zero_history[ 1 ] == 'Sys'   ):
                                Slave.Direction   = 'Forward'
                                return
                            elif ( Slave.Zero_history[ 0 ] == 'Slave' and Slave.Zero_history[ 1 ] == 'Slave' ):
                                Slave.Direction   = 'Backward'
                                return

    """--------------- DIRECTION - END ---------------"""

    """-------------------- ANGLE --------------------"""

    def angle( self, frame ): #private function

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
    	cnts   = cv2.findContours( thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    	cnts   = cnts[ 0 ] if imutils.is_cv2() else cnts[ 1 ]

#angle_of_planck

    	if cnts :
    		c = max( cnts, key = cv2.contourArea )
    		cv2.drawContours( mask, [ c ], -1, ( 255, 255, 255 ), -1 )


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
    		for c in contours:
        		con_area.append( cv2.contourArea( c ) )

    		max_area_index = con_area.index( max( con_area ) )

    		rect = cv2.minAreaRect( contours[ max_area_index ] )
    		box  = cv2.boxPoints( rect )
    		box  = np.int0( box)
    		cv2.drawContours( mask, [ box ], 0, ( 0, 0, 255 ), 2 )

    		tp1 = tp1+tuple( ( box[ 2 ] + box[ 3 ] ) / 2 )
    		tp2 = tp2+tuple( ( box[ 0 ] + box[ 1 ] ) / 2 )

    		tp3 = tp3+tuple( ( box[ 1 ] + box[ 2 ] ) / 2 )
    		tp4 = tp4+tuple( ( box[ 0 ] + box[ 3 ] ) / 2 )

    		if dist( tp1, tp2 ) > dist( tp3, tp4 ):
    		    pass
    		else:
    		    tp1 = tp3
    		    tp2 = tp4

    		value  = 0
    		height, width  = mask[ :2 ]
    		x_axis_of_mass = ( tp1[ 0 ] + tp2[ 0 ] ) / 2

    		if x_axis_of_mass < ( width.size / 2 ):
    		    if np.asarray( tp2 )[ 0 ] < np.asarray( tp1 )[ 0 ] :
    		        value = ( angle( np.asarray( tp2 ), np.asarray( tp1 ) ) )
    		        img   = cv2.arrowedLine( img, tp1, tp2, ( 124, 252, 0 ), 5 )
    		    else:
    		        value = ( angle( np.asarray( tp1 ), np.asarray( tp2 ) ) )
    		        img   = cv2.arrowedLine( img, tp2, tp1, ( 124, 252, 0 ), 5 )
    		else:
    		    if np.asarray( tp2 )[ 0 ] > np.asarray( tp1 )[ 0 ] :
    		        value = ( angle( np.asarray( tp2 ), np.asarray( tp1 ) ) )
    		        img   = cv2.arrowedLine( img, tp1, tp2, ( 124, 252, 0 ), 5 )
    		    else:
    		        value = ( angle( np.asarray( tp1 ), np.asarray( tp2 ) ) )
    		        img   = cv2.arrowedLine( img, tp2, tp1, ( 124, 252, 0 ), 5 )

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


            	Slave.Angle = value

        img = imutils.resize( img, width = 640 )
    	cv2.imshow( "Find_angle", img )


    	try:
    	    value # does a exist in the current namespace
    	except NameError:
    	    Slave.Angle = -9999999


    """----------------- ANGLE - END -----------------"""

    """--------------- WALL_POSITION -----------------"""

    def measure_wall_position( self, img ):
        return m_w_p( img )

    """------------ WALL_POSITION - END --------------"""

    """--------------- PLANK_POSITION ----------------"""

    def measure_plank_position( self, img ):

    	hsv         = cv2.cvtColor( img, cv2.COLOR_BGR2HSV )
    	lower_range = np.array( [ 0, 100, 100 ], dtype = np.uint8 )
    	upper_range = np.array( [ 10, 255, 255 ], dtype = np.uint8 )
    	mask_1      = cv2.inRange( hsv, lower_range, upper_range )
    	lower_range = np.array( [ 170, 100, 100 ], dtype = np.uint8 )
    	upper_range = np.array( [ 180, 255, 255] , dtype = np.uint8 )
    	mask_2      = cv2.inRange( hsv, lower_range, upper_range )
    	mask        = cv2.bitwise_or( mask_1, mask_2 )

    	gray   = mask
    	gray   = cv2.GaussianBlur( gray, ( 5, 5 ), 0 )
    	thresh = cv2.threshold( gray, 45, 255, cv2.THRESH_BINARY)[ 1 ]
    	thresh = cv2.erode( thresh, None, iterations = 2 )
    	thresh = cv2.dilate( thresh, None, iterations = 2 )
    	cnts   = cv2.findContours( thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    	cnts   = cnts[ 0 ] if imutils.is_cv2() else cnts[ 1 ]

    	c = max( cnts, key = cv2.contourArea )
    	cv2.drawContours( mask, [ c ], -1, ( 255, 255, 255 ), -1 )
    	image, contours, hier = cv2.findContours( mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )
    	con_area = []
    	for c in contours:
    		con_area.append( cv2.contourArea( c ) )

    	max_area_index = con_area.index( max( con_area ) )

    	rect = cv2.minAreaRect( contours[ max_area_index ] )
    	box  = cv2.boxPoints( rect )
    	box  = np.int0( box )

    	arr = [ box[ 0 ][ 1 ], box[ 1 ][ 1 ] ,box[ 2 ][ 1 ] ,box[ 3 ][ 1 ] ]
    	top_point_index = arr.index( min( arr ) )
    	arr.pop( top_point_index )
    	second_top_point_index = arr.index( min( arr ) )

    	if top_point_index <= second_top_point_index :
    		second_top_point_index += second_top_point_index

    	top_point = box[ top_point_index ]
    	second_top_point = box[ second_top_point_index ]
    	middle_point = ( box[ top_point_index ] + box[ second_top_point_index ] ) / 2
    	#print top_point,second_top_point,middle_point
    	#return middle_point
    	return middle_point[ 1 ]

    """------------ PLANK_POSITION - END -------------"""

    """------------------ ZERO_STOP ------------------"""

    def add_zero_dist( self, wall_position, plank_position ):
        distance = abs( wall_position - plank_position )
        Plank_and_wall.arr.append( distance )
        Plank_and_wall.arr.pop( 0 )

    def is_zero_stop( self , image_1, image_2 ):
        self.add_zero_dist( self.measure_wall_position( image_1 ), self.measure_plank_position( image_1 ) )
        self.add_zero_dist( self.measure_wall_position( image_2 ), self.measure_plank_position( image_2 ) )
        if ( Slave.Zero_history[ 0 ] == Slave.Zero_history[ 1 ] ):
            return True
        else:
            return False

    """--------------- ZERO_STOP - END ---------------"""

    """-------------------- STOP ---------------------"""

    def sys_clear( self ):
        Slave.Is_sys_stop  = False

    def is_stop( self ):
        ret, frame_1 = Slave.Angle_cam.read()
        self.angle( frame_1 )
        Angle_1 = Slave.Angle

        Slave.wait(time_for_process) #az bekle

        ret, frame_2 = Slave.Angle_cam.read()
        self.angle( frame_2 )
        Angle_2 = Slave.Angle

        Sys_condition = bool( ( Slave.Direction == 'Backward' and Angle_1 == 0 ) or ( abs ( Angle_1 ) == 90 ) )
        if ( Sys_condition ):
            Is_sys_stop  = True
            return True
        else:
            if ( Angle_1 == 0 ):
                if self.measure_wall_position( frame_1 ) is None: #wall_position_slave
                    return False
                else:
                    return self.is_zero_stop( frame_1, frame_2 )
            else:
                if ( Angle_1 == Angle_2 ):
                    return True
                else:
                    return False

    """----------------- STOP - END ------------------"""

if __name__ == "__main__":
    Robot = Slave()
    while(True):
	if Robot.obstacle():
	    Robot.turn( 25,0.55)
	    Robot.wait( 8 )
	else:
	    Robot.bang_bang(20,0)

"""
        front_dist = Robot.front_wall_dist()
        side_dist  = Robot.side_wall_dist()

        if front_dist <= 10 :
            if side_dist > 20 :
                Robot.motor(25,25,0,1)
            else:
                Robot.motor(25,25,1,0)
            time.sleep(0.75)

        else:
            if side_dist <= 11 :
                Robot.motor(40,20,1,1)
            elif side_dist >= 13 :
                Robot.motor(20,40,1,1)
            else:
                Robot.motor(30,30,1,1)
"""
"""
        # Capture frame-by-frame
        ret, frame = Robot.Angle_cam.read()
        ret, frames = Robot.Robot_cam.read()
        cv2.imshow('frame',frame)
        cv2.imshow('frames',frames)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
"""
"""
    Robot = Slave()
    while True:
        if Robot.obstacle():
            Robot.turn( speed,time_for_process)
            Robot.wait(time_for_process) #10sn
            #Robot.go_straight( speed,time_for_process)
            Robot.history_add_stop( 'Slave' )

        elif Robot.is_stop():
            Robot.wait(time_for_process) #10 sn tamamla
            Robot.detect_direction()
            if Robot.Is_sys_stop:
                Robot.history_add_stop( 'Sys' )
                Robot.sys_clear()

            else:
                Robot.history_add_stop( 'Master' )
            Robot.bang_bang( speed,time_for_process)


adjust the followings
1- speed
2- time
"""
