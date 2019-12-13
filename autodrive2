#!/usr/bin/env python

import rospy, time, cv2, rospkg, numpy as np
from std_msgs.msg import Int32MultiArray
from motordriver import MotorDriver
from linedetector import LineDetector
from obstacledetector import ObstacleDetector
import time


class AutoDrive:

    def __init__(self):
        rospy.init_node('xycar_driver')
        self.line_detector = LineDetector('/usb_cam/image_raw')
        self.obstacle_detector = ObstacleDetector('/ultrasonic')
        self.driver = MotorDriver('/xycar_motor_msg')
        self.savedata = [0]
        self.save_obs = 130

    def trace(self):
        obs_m = self.obstacle_detector.get_distance()
        
        if obs_m/2 >= 30 and int(obs_m) != 0:
            speed = int(obs_m/2) + 60
            self.save_obs = speed
            print(obs_m)
        else:
            speed = self.save_obs


        l_s,r_s = self.line_detector.run()
        
        
        if abs(l_s) >= 0.3 and abs(r_s) >= 0.3:
            if abs(l_s) > 2.5:
                angle = -8
                self.savedata[0] = angle
                
                #print("little left")
            elif abs(r_s) > 2.5:
                angle = 8
                self.savedata[0] = angle
                
                #print("little right")
            else:
                angle = 0
                self.savedata[0] = angle
                
                #print("go")
        elif (l_s == 0) and (r_s == 0):
            angle = self.savedata[0]
            #print("maybe go 111")

        elif (l_s == 0):
            angle = -50
            self.savedata[0] = angle
            
            #print("left")

        elif (r_s == 0):
            angle = 50
            self.savedata[0] = angle
            
            #print("right")

        
        else:
            if abs(l_s) < 0.3:
                angle = 50
                self.savedata[0] = angle
                
                #print("maybe right")
            elif abs(r_s) < 0.3:
                angle = -50
                self.savedata[0] = angle
                
                #print("maybe left")
            else:
                angle = self.savedata[0]
                
                #print("maybe go 222")
        
        self.sum = (r_s + l_s)
        
        self.driver.drive(90 + angle, speed)

    def exit(self):
        print('finished')

if __name__ == '__main__':
    car = AutoDrive()
    time.sleep(3)
    rate = rospy.Rate(15)
    while not rospy.is_shutdown():
        car.trace()
        rate.sleep()
	
    rospy.on_shutdown(car.exit)
