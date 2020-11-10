import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import tf
import math

odom = Odometry()
scan = LaserScan()

kp = 0.01

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
    yaw = getAngle(odom)
    setpoint = 120
    error = (setpoint-yaw)
    
    if abs(error) > 180:
        error = -error
        
    P = kp*error
    I = 0
    D = 0
    
    control = P+I+D
    
    msg = Twist()
    msg.angular.z = control
    pub.publish(msg)

    
    
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
odom_sub = rospy.Subscriber('/odom', Odometry, odomCallBack)
scan_sub = rospy.Subscriber('/Scan', LaserScan, scanCallBack)

timer = rospy.Timer(rospy.Duration(0.05), timerCallBack)

rospy.spin()
