import cv2
import numpy as np
 
cap = cv2.VideoCapture(0)


class Trafficlight:
    def __init__(self, topic):
        # Initialize various class-defined attributes, and then...
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
        self.found = [False, False] # red green
        rospy.Subscriber(topic, Image, self.conv_image)
        
    def conv_image(self, img)
        l_g = np.array([50, 0, 0]) 
        u_g = np.array([70, 255, 255])

        l_r = np.array([-10, 50, 50])
        u_r = np.array([10, 255, 150])
        self.found = [False, False] # red green
        img = cv2.GaussianBlur(img,(5,5),0)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow('gray', gray)
        circles1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,1,20,
                                    param1=40,param2=75,minRadius=0,maxRadius=0)
        
        

        if circles1 is not None:
            circles1 = np.uint16(np.around(circles1))
            for c in circles1[0,:]:
                hue = np.average(img_hsv[c[1], c[0]-c[2]+1:c[0]+c[2]-1, 0])
                sat = np.average(img_hsv[c[1], c[0]-c[2]+1:c[0]+c[2]-1, 1])
                val = np.average(img_hsv[c[1], c[0]-c[2]+1:c[0]+c[2]-1, 2])
                if (168<hue and hue<175) and sat>30 and val>40:
                    print('red', hue)
                    cv2.circle(img,(c[0],c[1]),c[2],(0,0,255),2)
                    found[0] = True
                if (57<hue and hue<61) and sat>50 and val>80:
                    print('green', hue)
                    cv2.circle(img,(c[0],c[1]),c[2],(0,255,0),2) 
                    found[1] = True
        cv2.imshow('detected circles', img)
        cv2.waitKey(1)

cap.realeae()
cv2.destroyAllWindows()