#!/usr/bin/env python                                                                           
import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import String
from std_msgs.msg import Empty
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist
from ar_track_alvar_msgs.msg import AlvarMarkers
import time
import math
count = 0
limit_count = 0


class ArTracking():
    def __init__(self):
        rospy.init_node('ar_tracking')
        rospy.loginfo('activate')
        self.ar_detect = False
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
        self.ar_sub = rospy.Subscriber('/ar_pose_marker',AlvarMarkers,self.callback)

    def callback(self, msg):
        global count,limit_count
        ar_pose = msg.markers
        twist = Twist()
        if ar_pose:
            rospy.loginfo("detected")
            pose = ar_pose[0].pose.pose
            position = pose.position
            px = position.x
            #linear.y = rpm(), angular.z = stepping(-1,0,1)
            if px < -0.05 or 0.05 < px:
                twist.angular.z = px/abs(px) * -1
                twist.linear.y = 0.0
            else:
                twist.linear.y = 180
                twist.angular.z = 0.0
            rospy.loginfo(twist.angular.z)
        self.cmd_vel_pub.publish(twist)
            
if __name__=="__main__":
    try:
        ar = ArTracking();
        rospy.spin()
    except rospy.ROSInterruptException: pass
