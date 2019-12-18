import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ColorDetector:

    def __init__(self, topic):
        # Initialize various class-defined attributes, and then...
        self.lower_red = np.array([120, 100, 0])
        self.upper_red = np.array([255, 255, 255])
        self.cam_img = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        self.mask = np.zeros(shape=(480, 640),
                             dtype=np.uint8)
        self.edge = np.zeros(shape=(480, 640),
                             dtype=np.uint8)
        self.bridge = CvBridge()
        self.roi_vertical_pos = 0
        self.scan_height = 0
        self.num=[[],[]]
        self.idx = 0
        rospy.Subscriber(topic, Image, self.conv_image)

    def run (self):

        img_color = self.cam_img
        height, width = img_color.shape[:2]
        #img_color = cv2.resize(img_color, (width, height), interpolation=cv2.INTER_AREA)
        img_blurred = cv2.GaussianBlur(img_color, (7,7), 0)
        img_hsv = cv2.cvtColor(img_blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, self.lower_red, self.upper_red)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        #cv2.imshow('test',mask)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(cnts)>0 :
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            x = center[0]
            cv2.circle(img_color, (int(x), int(y)), int(radius), (255, 0, 0), 2)
            print(int(x), int(y), int(radius))
            return int(x), int(radius)
        else:
            x = None
            radius = None
            return x, radius

        #cv2.imshow('img_color',img_color)

        #if cv2.waitKey(1) & 0xFF == 27 :
            #pass

        #return center


    def conv_image(self,data):
        self.cam_img = self.bridge.imgmsg_to_cv2(data, 'bgr8')

    def detect_lines(self):
        return -1, -1
