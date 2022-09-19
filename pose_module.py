from traceback import print_tb
import cv2 as cv
import mediapipe as mp
import time
import math
import numpy as np
 
 
class poseDetector():
    
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
 
        self.mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
        self.mpPose = mp.solutions.mediapipe.python.solutions.pose
        self.pose = self.mpPose.Pose(self.static_image_mode,self.model_complexity, self.smooth_landmarks,
                                      self.enable_segmetation, self.smooth_segmentation, self.min_detection_confidence,self.min_tracking_confidence)
        self.red = [0,0,255]
        self.blue = [255,0,0]
 
    def nothing(self):
        pass
    
    def findPose(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img
 
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 5, (255, 0, 0), cv.FILLED)
        return self.lmList
 
    def findAngle(self, img, p1, p2, p3, draw=True):
 
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
 
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
 
        # print(angle)
 
        # Draw
        if draw:
            cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv.circle(img, (x1, y1), 10, (0, 0, 255), cv.FILLED)
            cv.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv.circle(img, (x2, y2), 10, (0, 0, 255), cv.FILLED)
            cv.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv.circle(img, (x3, y3), 10, (0, 0, 255), cv.FILLED)
            cv.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle
    def nothing():
        pass
        

def main():
    video_path = "/home/kosmos/Videos/sample.mp4"
    video_path2 = '/home/kosmos/Videos/Webcam/hasrob1.webm'
    video_path3 = '/home/kosmos/Videos/Webcam/hasrob2.webm'
    cap = cv.VideoCapture(video_path2)
    pTime = 0
    detector = poseDetector()
    
    red = [0,0,255]
    
    platform = False
    
    window = "trackbar"
    cv.namedWindow(window)
    cv.createTrackbar('hue min',window,0,179,detector.nothing)
    cv.createTrackbar('sat min',window,4,255,detector.nothing)
    cv.createTrackbar('val min',window,197,255,detector.nothing)
    cv.createTrackbar('hue max',window,37,179,detector.nothing)
    cv.createTrackbar('sat max',window,20,255,detector.nothing)
    cv.createTrackbar('val max',window,255,255,detector.nothing)
    
    while True:
        success, img = cap.read()
        if not success:
            print("capture failed")
            break
        
        width = 900
        height = 600
        img_size = (width,height)
        img = cv.resize(img,img_size,interpolation=cv.INTER_AREA)
    
        blur = cv.GaussianBlur(img,(5,5),0)
        img_hsv = cv.cvtColor(blur,cv.COLOR_BGR2HSV)
        hmin = cv.getTrackbarPos('hue min',window)
        smin = cv.getTrackbarPos('sat min',window)
        vmin = cv.getTrackbarPos('val min',window)
        hmax = cv.getTrackbarPos('hue max',window)
        smax = cv.getTrackbarPos('sat max',window)
        vmax = cv.getTrackbarPos('val max',window)
        
        low = np.array([hmin,smin,vmin])
        high = np.array([hmax,smax,vmax])
        img_mask = cv.inRange(img_hsv,low,high)
        cv.imshow(window,img_mask)
        
        cv.putText(img,"platform status: ",(30,50),cv.FONT_HERSHEY_PLAIN,3,red,3)
        
        drawing = img.copy()
        contour = cv.findContours(img_mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)[0]
        for c in contour:
            area = cv.contourArea(c)
            cv.drawContours(drawing,[c],-1,red,3)
            cv.imshow("drawing",drawing)
            
            if area > 3500:
                print(area)
                platform = True
        
        if platform == True:
            cv.putText(img,"present",(450,50),cv.FONT_HERSHEY_PLAIN,3,red,3)
            print("platform present, please becareful!")
            
        elif platform == False:
            cv.putText(img,"absent",(450,50),cv.FONT_HERSHEY_PLAIN,3,red,3)
            cv.line(img,(225,550),(675,550),[255,255,255],3)
            img = detector.findPose(img)
            lmList = detector.findPosition(img, draw=False)
            if len(lmList) != 0:
                # print(lmList[28])
                cv.circle(img, (lmList[27][1], lmList[27][2]), 15, (0, 0, 255), cv.FILLED)
                cv.circle(img, (lmList[28][1], lmList[28][2]), 15, (0, 0, 255), cv.FILLED)
                if lmList[27][2] and lmList[28][2] < 550:
                    print("WARNING: unsafe action!!!")
 
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
 
        cv.putText(img, str(int(fps)), (850, 50), cv.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
 
        cv.imshow("Image", img)
        cv.waitKey(150)
 
 
if __name__ == "__main__":
    main()
