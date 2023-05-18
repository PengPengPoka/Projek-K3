from math import fabs
from re import X
import cv2 as cv
import mediapipe as mp
import time

class PoseDetect:
    def __init__(self, static_image_mode = False, model_complexity = 0, smooth_landmarks = True, 
                 enable_segmetation = False,smooth_segmentation = False,
                 min_detection_confidence = 0.5, min_tracking_confidence = 0.5):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmetation = enable_segmetation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        
        self.mp_pose = mp.solutions.mediapipe.python.solutions.pose
        self.mp_draw = mp.solutions.mediapipe.python.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(self.static_image_mode,self.model_complexity, self.smooth_landmarks,
                                      self.enable_segmetation, self.smooth_segmentation, self.min_detection_confidence,self.min_tracking_confidence)
        
    def find_pose(self, img, draw=True):
        img_rgb = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)
        if self.results.pose_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(img,self.results.pose_landmarks,self.mp_pose.POSE_CONNECTIONS)
        return img 

cap = cv.VideoCapture(0)
detect = PoseDetect()
    
while True:
    grab, img = cap.read()
    if not grab:
        print("image not grabbed")
        
    img = detect.find_pose(img)
        # landmark_ls = detect.
        
    cv.imshow("image",img)
    cv.waitKey(150)
            