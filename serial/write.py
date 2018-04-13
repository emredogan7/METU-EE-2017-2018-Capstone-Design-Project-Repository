import serial
import time
ser = serial.Serial('/dev/ttyUSB0',9600)
degree = 180
    
while ( 1 ) :
    ser.write( str(degree).encode() );
    time.sleep(1);
