#!/usr/bin/env python                                                                           
import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import String
from std_msgs.msg import Empty
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist
from jsk_recognition_msgs.msg import RectArray
import time
import math
limit_count = 0


class FaceDetection():
    def __init__(self):
        self.count = 0
        self.cmd_state = False
        self.face_list = []
        self.face_id_relate = []
        self.id_count = [0,0,0,0,0]
        rospy.init_node('sleeping_detecter')
        rospy.loginfo('activate')
        self.twist_sub = rospy.Subscriber('/cmd_vel', Twist,self.callback_cmd)
        self.face_sub = rospy.Subscriber('/edgetpu_face_detector/output/rects',RectArray,self.callback_face)
        self.id_pub = rospy.Publisher('/sleeping_id', UInt8, queue_size = 10)


    def callback_cmd(self, msg):
        linear_y = msg.linear.y
        angular_z = msg.angular.z
        """
        if (linear_y not 0) or (angular_z not 0):
            self.cmd_state = True
        """
    def callback_face(self, msg):
        rects = msg.rects
        if len(rects) == 6 and self.count == 0:
            self.count  = 1
            for i, item in enumerate(rects):
                x = item.x
                y = item.y
                w = item.width
                h = item.height
                self.face_list.append([x,y,w,h])
            self.face_list = sorted(self.face_list, key=lambda x:(x[1]))
            face_upper = sorted(self.face_list[0:2], key=lambda x:(x[0]))
            fece_down = sorted(self.face_list[2:4], key=lambda x:(x[0]))
            for i, item in enumerate(face_upper):
                self.face_id_relate.append(item)
            for i, item in enumerate(face_down):
                self.face_id_relate.append(item)
        if self.count:
            for i in range(len(self.id_count)):
                self.id_count[i] += 1
            for i, rect in enumerate(rects):
                for j , face in enumerate(self.face_id_relate):
                    if (face[0]-face[2]/2 < rect.x < face[0]+face[2]/2) and (face[1]-face[3]/2 < rect.y < face[1] +face[3]/2):
                        self.id_count[j] = 0
                        break
            for i , face_id in enumerate(self.id_count):
               if face_id > 100 and (not self.cmd_state):
                   self.id_pub.publish(i)
                   break
               if i == len(self.id_count) and (not self.cmd_state):
                   self.id_pub.publish(-1)
        
            
            
if __name__=="__main__":
    try:
        face_detection = FaceDetection();
        rospy.spin()
    except rospy.ROSInterruptException: pass
