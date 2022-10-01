import audioplayer
from platform import platform
import time
import cv2 as cv
import numpy as np
from pose_module import poseDetector

def nothing():
    pass

video_path2 = '/home/kosmos/Videos/Webcam/hasrob1.webm'
video_path3 = '/home/kosmos/Videos/Webcam/hasrob2.webm'

cap = cv.VideoCapture(video_path3)
pTime = 0
pd = poseDetector()

red = [0,0,255]
window = "trackbar"
platform_stat = False

cv.namedWindow(window)
cv.createTrackbar('hue min',window,0,179,nothing)
cv.createTrackbar('sat min',window,4,255,nothing)
cv.createTrackbar('val min',window,197,255,nothing)
cv.createTrackbar('hue max',window,37,179,nothing)
cv.createTrackbar('sat max',window,20,255,nothing)
cv.createTrackbar('val max',window,255,255,nothing)

while cap.isOpened():
    grab, frame = cap.read()
    if not grab:
        print("capture failed")
        break
    
    width = 900
    height = 600
    frame_size = (width,height)
    frame = cv.resize(frame,frame_size,interpolation=cv.INTER_AREA)

    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    hmin = cv.getTrackbarPos('hue min',window)
    smin = cv.getTrackbarPos('sat min',window)
    vmin = cv.getTrackbarPos('val min',window)
    hmax = cv.getTrackbarPos('hue max',window)
    smax = cv.getTrackbarPos('sat max',window)
    vmax = cv.getTrackbarPos('val max',window)

    low = np.array([hmin,smin,vmin])
    high = np.array([hmax,smax,vmax])
    thresh = cv.inRange(hsv,low,high)
    cv.imshow(window,thresh)

    cv.putText(frame,"platform status: ",(30,50),cv.FONT_HERSHEY_PLAIN,3,red,3)

    drawing = frame.copy()
    contour = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)[0]
    for c in contour:
        area = cv.contourArea(c)
        cv.drawContours(drawing,[c],-1,red,3)
        
        if area > 3500:
            print(area)
            platform = True

    if platform == True:
        cv.putText(frame,"present",(450,50),cv.FONT_HERSHEY_PLAIN,3,red,3)
        print("platform present, please becareful!")
        
    elif platform_stat == False:
        cv.putText(frame,"absent",(450,50),cv.FONT_HERSHEY_PLAIN,3,red,3)
        cv.line(frame,(225,550),(675,550),[255,255,255],3)
        
        frame = pd.findPose(frame)
        lmlist =pd.findPosition(frame,draw=False)
        if len(lmlist) != 0:
            cv.circle(frame, (lmlist[27][1], lmlist[27][2]), 15, (0, 0, 255), cv.FILLED)
            cv.circle(frame, (lmlist[28][1], lmlist[28][2]), 15, (0, 0, 255), cv.FILLED)
            if lmlist[27][2] and lmlist[28][2] < 550:
                print("WARNING: unsafe action!!!")
        

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(frame,str(int(fps)),(800,50),cv.FONT_HERSHEY_PLAIN,3,(255, 0, 0),3)
    
    cv.imshow("video",frame)
    cv.waitKey(30)