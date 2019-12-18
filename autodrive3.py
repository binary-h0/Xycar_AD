#!/usr/bin/env python

import rospy, time, cv2, rospkg, numpy as np
from std_msgs.msg import Int32MultiArray
from motordriver import MotorDriver
#from linedetector import LineDetector
#from obstacledetector import ObstacleDetector
from colorDectector import ColorDetector
import time


class AutoDrive:

    def __init__(self):
        rospy.init_node('xycar_driver')
        self.color_detector = ColorDetector('/usb_cam/image_raw')
        #self.obstacle_detector = ObstacleDetector('/ultrasonic')
        #self.color_detector = ColorDectector()
        self.driver = MotorDriver('/xycar_motor_msg')
        #self.savedata = [0]
        #self.save_obs = 130
    def trace(self):
        cir_x, cir_r = self.color_detector.run()
        if (cir_x != None):
            if cir_r < 40:
                angle = 90 + float(50) / 320 * (cir_x -320)
                speed = 125
            else:
                angle = 90
                speed = 90
        else:
            angle = 90
            speed = 90
        self.driver.drive(angle, speed)

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