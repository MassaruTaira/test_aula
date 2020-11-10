import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import tf
import math

odom = Odometry()
scan = LaserScan()

kp = 0.5

rospy.init_node('cmd_node')

#----------AUXILIAR Function-----------------------------------------------------
def getAngle(msg):
    quaternion = msg.pose.pose.orientation
    quat = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
    euler = tf.transformations.euler_from_quaternion(quat)
    yaw = euler[2]*180.0/math.pi
    return yaw
    
    
#----------CALLBACKS-------------------------------------------------------------

def odomCallBack(msg):
    global odom
    odom = msg
    
    
def scanCallBack(msg):
    global scan
    scan = msg
#--------------------------------------------------------------------------------


#---------TIMER - CONTROL LOOP---------------------------------------------------
def timerCallBack(event):
    """
    yaw = getAngle(odom)
    setpoint = -45
    error = (setpoint-yaw)
    
    if abs(error) > 180:
        if setpoint < 0:
            error += 360
        else:
            error -= 360
    """
    """
    setpoint = (-1,-1)
    position = odom.pose.pose.position
    dist = setpoint[0] - position.x #math.sqrt((setpoint[0] - position.x)**2  + (setpoint[1] - position.y)**2)
    error = dist
    """
    
    
    setpoint = 0.5
    
    scan_len = len(scan.ranges)
    read = min(scan_len)
    if read > 0:
    
        error = -(setpoint - read)
        
        P = kp*error
        I = 0
        D = 0
            
        control = P+I+D
        if control > 1:
            control = 1
        elif control < -1:
            control = -1
            
    else:
        control = 0

    
    
    msg = Twist()
    msg.linear.x = control
    pub.publish(msg)

    
    
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
odom_sub = rospy.Subscriber('/odom', Odometry, odomCallBack)
scan_sub = rospy.Subscriber('/Scan', LaserScan, scanCallBack)

timer = rospy.Timer(rospy.Duration(0.05), timerCallBack)

rospy.spin()
