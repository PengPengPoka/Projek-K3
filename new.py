from re import S
import threading
from attr import s
import audioplayer as ap
import time
import cv2 as cv
import numpy as np
from pose_module import poseDetector
import socket

def nothing():
    pass

def playAudio(audio):
    audio.play(False,True)
    time.sleep(5)
    
def process(cap):
    pTime = 0
    pd = poseDetector()
    
    red = [0,0,255]
    window = "trackbar"
    platform_stat = False
    
    global s
    s = -1
    
    cv.namedWindow(window)
    cv.createTrackbar('hue min',window,32,179,nothing)
    cv.createTrackbar('sat min',window,0,255,nothing)
    cv.createTrackbar('val min',window,176,255,nothing)
    cv.createTrackbar('hue max',window,74,179,nothing)
    cv.createTrackbar('sat max',window,44,255,nothing)
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
            
            if area > 4500:
                platform_stat = True

        if platform_stat == True:
            cv.putText(frame,"present",(450,50),cv.FONT_HERSHEY_PLAIN,3,red,3)
            print("platform present, please becareful!")
            s = 0
            return s
            # file.writelines("0\n")
            # playAudio(audio_safe,event)
            
        elif platform_stat == False:
            cv.putText(frame,"absent",(450,50),cv.FONT_HERSHEY_PLAIN,3,red,3)
            # cv.line(frame,(225,460),(675,460),[0,0,255],3)
            cv.line(frame,(225,550),(675,550),[0,0,255],3)
            
            frame = pd.findPose(frame)
            lmlist = pd.findPosition(frame,draw=False)
            if len(lmlist) != 0:
                cv.circle(frame, (lmlist[27][1], lmlist[27][2]), 15, (0, 0, 255), cv.FILLED)
                cv.circle(frame, (lmlist[28][1], lmlist[28][2]), 15, (0, 0, 255), cv.FILLED)
                if lmlist[27][2] and lmlist[28][2] < 550:
                    print("WARNING: unsafe action!!!")
                    s = 1
                    return s
                    # file.writelines("1\n")
                    # playAudio(audio_safe,event)
            
        platform_stat = False


        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(frame,str(int(fps)),(800,50),cv.FONT_HERSHEY_PLAIN,3,(255, 0, 0),3)
        
        cv.imshow("video",frame)
        cv.waitKey(150)

    
video_path2 = '/home/kosmos/Videos/Webcam/hasrob1.webm'
video_path3 = '/home/kosmos/Videos/Webcam/hasrob2.webm'
video_path4 = '/home/kosmos/Videos/Webcam/orang.webm'
video_path5 = '/home/kosmos/Videos/Webcam/kosong.webm'
video_path6 = '/home/kosmos/Videos/Webcam/kursi.webm'
safe = "aman.mpeg"
unsafe = "tidak aman.mpeg"

cap = cv.VideoCapture(video_path2)
process(cap)


# t1 = threading.Thread(target=process)
# t1.start()

# t1.join()