#!/usr/bin/env python
import roslib;
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import NavSatFix
from math import pi, tan, atan
import serial
from std_msgs.msg import Float64
from std_msgs.msg import Int16


port = '/dev/ttyACM0'


s = serial.Serial(port,9600,timeout=5)

max_steer_angle=80
max_speed=1
L=0.31  #Length of vehicle in m
#test with rostopic pub -r 1 cmd_vel geometry_msgs/Twist '{linear: {x: 0.1, y: 0, z: 0}, angular: {x: 0, y: 0, z: 1}}'
# rostopic pub mav_led std_msgs/Int8 3

global led1
global led2
global led3
led1=0
led2=0
led3=0
def callbackled(msg):
    global led1
    global led2
    global led3
    bit_mask = int('00000001', 2)  # Bit 1
    if(bit_mask & msg.data):
      led1=1
    else:
      led1=0
    bit_mask = int('00000010', 2)  # Bit 1
    if(bit_mask & msg.data):
      led2=1
    else:
      led2=0
    bit_mask = int('00000100', 2)  # Bit 1
    if(bit_mask & msg.data):
      led3=1
    else:
      led3=0
def send_mav_callback(msg):
    #Steer section
    #Convert z dot into a physical steer angle, Positive steers to the right, negative to the left
    #z dot in radians
    if msg.linear.x != 0:
    	steer_angle= -atan(msg.angular.z*L/msg.linear.x)*57.296
    else:
	steer_angle=0
    
    #the vehicle uses PWM values 0=hard left, 128=centre, 255=hard right
    #Hard left/right is +40 to -40 deg
    if steer_angle<-max_steer_angle: steer_angle=-max_steer_angle
    if steer_angle>max_steer_angle: steer_angle=max_steer_angle
    #steer_angle=msg.angular.z
    steer_b=int(steer_angle)
    print ('Steer angle=%d'%(steer_angle))
    #Speed section
    #PWM values: Full rev=0, stop=128, full fwd=255
    speed=msg.linear.x   #m/s
    if speed<-max_speed: speed=-max_speed
    if speed>max_speed: speed=max_speed
    
    speed_b=int(speed)
    
   
    
    #steer_b=int(steer_b)
    #speed_b=int(speed_b)
     ##Thoughts: conversion should be on arduino as its HW specific
    s.write('$%d,%f,%d,%d,%d:'%(steer_b,speed,led1,led2,led3))
    #s.writeline('$%d,0.1,1,1,1,NIL\n'%steer_b)
    print('$%d,%f,1,1,1,NIL\n'%(steer_b,speed))
    #rospy.loginfo("Received a /cmd_vel message!")
    #rospy.loginfo("Linear Components: [%f, %f, %f]"%(msg.linear.x, msg.linear.y, msg.linear.z))
    #rospy.loginfo("Angular Components: [%f, %f, %f]"%(msg.angular.x, msg.angular.y, msg.angular.z))
    #rospy.loginfo("sending: [%d,%d]"%(steer_b,speed_b))
    

def ar_data_split(nmea):
	lat=0
	lon=0
	bearing=0
	nmea = nmea.split(",")
	#TODO: would be better to use regex instead of split for error handling
	if len(nmea)<3:
		print "error invalid input"
		#if unknown return lat,lon as 0,0 which is a valid cordinate but you will notice the error unless you are in Grewnich
		return 0,0,0
	if len(nmea)==3 and nmea[0]:
	 
	 Lats,Lons,bearings = nmea[0:3]
      
	 #if type is GPRMC calculate lat,lon
	 #print(UTMLats)
	 lat=float(Lats)
	 #print(UTMLat)
	 lon=float(Lons)
	 bearing=int(bearings)
	 

	return lat,lon,bearing



rospy.init_node('mav_publisher')
publt=rospy.Publisher('lat',Float64,queue_size=1)
publn=rospy.Publisher('lon',Float64,queue_size=1)
pubbr=rospy.Publisher('bear',Int16,queue_size=1)
pubgps=rospy.Publisher('gps',NavSatFix,queue_size=1)
rate=rospy.Rate(10)

s.close()
s.open()
s.flush()
rospy.Subscriber("/cmd_vel", Twist, send_mav_callback)
rospy.Subscriber("/mav_led", Int16, callbackled)
current_fix=NavSatFix()
while not rospy.is_shutdown():
	data=s.readline()
        lt,ln,br=ar_data_split(data)
	print(br)
	#print(led1)
	publt.publish(lt)
	publn.publish(ln)
	pubbr.publish(br)

	current_fix.latitude=lt
	current_fix.longitude=ln
	
	pubgps.publish(current_fix)
	rate.sleep()
s.close()




