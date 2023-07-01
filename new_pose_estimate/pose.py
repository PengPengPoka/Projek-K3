import cv2 as cv
import mediapipe as mp
from playsound import playsound
import time
import threading
from threading import Timer
import numpy as np

from pose_module import PoseDetector

safe = "/home/kosmos/vision/Projek-K3/utils/sound/aman.mpeg"
unsafe = "/home/kosmos/vision/Projek-K3/utils/sound/tidak aman.mpeg"

def nothing():
    pass

def millis():
    return round(time.time()*1000)

def audio(action):
    if action == -1:
        pass
    elif action == 0:
        playsound(safe)
    elif action == 1:
        playsound(unsafe)
    time.sleep(3)

def main():


    path0 = "/home/kosmos/Videos/man walking.webm"
    path1 = "/home/kosmos/Videos/ivan manjat.MOV"
    path2 = "/home/kosmos/Videos/Webcam/manjat kasur.webm"
    path3 = "/home/kosmos/Videos/Webcam/manjat kursi.webm"
    path4 = "/home/kosmos/Videos/Webcam/manjat kursi2.webm"
    path5 = "/home/kosmos/Videos/Webcam/manjat kursi3.webm"
    cap = cv.VideoCapture(path1)

    pd = PoseDetector()
    pTime = 0
    platform_status = False
    red = [0,0,255]
    window = "trackbar"

    action = -1
    i = 0

    cv.namedWindow(window)
    cv.createTrackbar('hue min',window,0,179,nothing)
    cv.createTrackbar('sat min',window,0,255,nothing)
    cv.createTrackbar('val min',window,0,255,nothing)
    
    cv.createTrackbar('hue max',window,0,179,nothing)
    cv.createTrackbar('sat max',window,0,255,nothing)
    cv.createTrackbar('val max',window,0,255,nothing)

    while cap.isOpened():
        grab, frame = cap.read()
        if not grab:
            print("capture failed")
            break

        dimension = (900,600)
        frame = cv.resize(frame,dimension,interpolation=cv.INTER_AREA)

        hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        hmin = cv.getTrackbarPos('hue min',window)
        smin = cv.getTrackbarPos('sat min',window)
        vmin = cv.getTrackbarPos('val min',window)

        hmax = cv.getTrackbarPos('hue max',window)
        smax = cv.getTrackbarPos('sat max',window)
        vmax = cv.getTrackbarPos('val max',window)

        low = np.array([98,134,0])
        high = np.array([129,255,112])
        thresh = cv.inRange(hsv,low,high)
        cv.imshow(window,thresh)
        cv.putText(frame,"platform status: ",(30,50),cv.FONT_HERSHEY_PLAIN,3,red,3)

        drawing = frame.copy()
        contour = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)[0]
        for c in contour:
            area = cv.contourArea(c)
            cv.drawContours(drawing,[c],-1,red,3)
            if area > 1500 and area < 30000:
                # print(area)
                platform_status = True
        
        if platform_status == True:
            cv.putText(frame,"present",(450,50),cv.FONT_HERSHEY_PLAIN,3,red,3)
            print("platform present, please becareful!")
            action = 0

        elif platform_status == False:
            cv.putText(frame,"absent",(450,50),cv.FONT_HERSHEY_PLAIN,3,red,3)
            # cv.line(frame,(225,460),(675,460),[0,0,255],3)
            cv.line(frame,(225,550),(675,550),[0,0,255],3)

            action = 1
            frame = pd.findPose(frame)
            lmlist = pd.findPosition(frame,False)
            if len(lmlist) != 0:
                cv.circle(frame, (lmlist[27][1], lmlist[27][2]), 15, (0, 0, 255), cv.FILLED)
                cv.circle(frame, (lmlist[28][1], lmlist[28][2]), 15, (0, 0, 255), cv.FILLED)
                if lmlist[27][2] and lmlist[28][2] < 550:      #parameter tidak aman
                    print("WARNING: unsafe action!!!")

        platform_status = False

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(frame,str(int(fps)),(800,50),cv.FONT_HERSHEY_PLAIN,3,(255, 0, 0),3)

        tAudio = threading.Thread(target=audio,args=(action,))
        # tTime = Timer(1,)
        i += 1
        if i == 100: 
            tAudio.start()
            i = 0
            # action = -1

        print(i)
        cv.imshow("video",frame)
        # cv.imshow("contour",drawing)
        cv.waitKey(30)


if __name__ == "__main__":
    main()