#!/usr/bin/env python

import rospy, time, cv2, rospkg, numpy as np
from std_msgs.msg import Int32MultiArray
from motordriver import MotorDriver
#from linedetector import LineDetector
#from obstacledetector import ObstacleDetector
from colorDectector import ColorDectector
import time


class AutoDrive:

    def __init__(self):
        rospy.init_node('xycar_driver')
        #self.line_detector = LineDetector('/usb_cam/image_raw')
        #self.obstacle_detector = ObstacleDetector('/ultrasonic')
        self.color_detector = ColorDectector()
        self.driver = MotorDriver('/xycar_motor_msg')
        self.savedata = [0]
        self.save_obs = 130

    def trace(self):
        cir_x, cir_y, cir_r = self.color_detector.fine_red()

        if cir_r > 기준 반지름:

            if 중심선 - 10 <= cir_x <= 중심선 + 10: # 느린 직진
                angle = 0
                speed =

            elif cir_x < 중심선 - 10:진 # 느린 좌회전
                angle =
                speed =

            elif cir_x > 중심선 + 10:전 # 느린 우회전

        elif cir_r <= 기준 반지름:

            if 중심선 - 10 <= cir_x <= 중심선 + 10: # 빠른 직진
                angle = 0
                speed =

            elif cir_x < 중심선 - 10: # 빠른 좌회전
                angle =
                speed =

            elif cir_x > 중심선 + 10: # 빠른 우호전
                angle =
                speed =

        elif cir_r >= 초과 반지름: # 정지 후 후진
            angle =
            speed =

        self.driver.drive(90 + angle, 90 + speed)

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
