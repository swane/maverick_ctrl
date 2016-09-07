# maverick_ctrl
ROS Arduino bridge for the Maverick robot
ROS and Maverick
Communication between Arduino and Linux PC  
Arduino code
All data is sent and received via the com port ACM0
Data to send to Maverick

Item
Data type
Steer angle
Int -80 to +80
Speed
Double -1.0 to 1.0 single precision
Led 1,2,3 on/off
Boolean, 0/1 separated by comma

Start of transmission ‘$’. End of transmission colon ':'.
e.g. to steer at 30 degrees at a speed of 0.5 m/s and all leds on, send to ACM0:
$30,0.5,1,1,1:
ROS node maverick_ctrl.py
Node name: mav_publisher

Data sent:
Twist message

Data received:
Topic NavSatFix
  .latitude
  .longitude

Int16 bearing

